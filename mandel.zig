const std = @import("std");
const Complex = std.math.Complex(f64);

fn norm(c: Complex) f64 {
    return c.re * c.re + c.im * c.im;
}

fn mandelbrot(
    width: usize,
    height: usize,
    bitmap: []u8,
) !void {
    const max_iterations = 50;
    const limit: f64 = 4;
    for (0..height) |y| {
        for (0..width) |x| {
            var Z = Complex{ .re = 0, .im = 0 };
            const C = Complex{
                .re = 2 * @intToFloat(f64, x) / @intToFloat(f64, width) - 1.5,
                .im = 2 * @intToFloat(f64, y) / @intToFloat(f64, height) - 1.0,
            };

            var i: usize = 0;
            while (i < max_iterations and norm(Z) <= limit) : (i += 1) {
                Z = Z.mul(Z).add(C);
            }

            bitmap[y * width + x] = @boolToInt(norm(Z) <= limit);
        }
    }
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const args = try std.process.argsAlloc(allocator);
    defer std.process.argsFree(allocator, args);

    if (args.len != 2) {
        std.debug.print("usage: {s} [width/height]\n", .{args[0]});
        std.process.exit(1);
    }

    const width_height = try std.fmt.parseInt(usize, args[1], 10);
    if (width_height % 8 != 0) {
        std.debug.print("width/height must be divisible by 8\n", .{});
        std.process.exit(1);
    }

    var bitmap = try allocator.alloc(u8, width_height * width_height);
    defer allocator.free(bitmap);

    var timer = try std.time.Timer.start();
    try @call(.never_inline, mandelbrot, .{ width_height, width_height, bitmap });
    const elapsed_ns = timer.lap();

    std.debug.print("Elapsed ms: {}\n", .{elapsed_ns / std.time.ns_per_ms});

    var output_file = try std.fs.cwd().createFile("mandelbrot.pbm", .{});
    var buffered_writer = std.io.bufferedWriter(output_file.writer());
    const writer = buffered_writer.writer();
    try writer.print("P4\n{} {}\n", .{ width_height, width_height });

    var byte: u8 = 0;
    for (bitmap, 0..) |bit, i| {
        byte = byte << 1 | bit;
        if (i % 8 == 7) {
            try writer.writeByte(byte);
            byte = 0;
        }
    }

    try buffered_writer.flush();
}
