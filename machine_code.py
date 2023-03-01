test_numbers = [-2, -1, 0, 1, 2]

def norm_spec(real, imag):
    return real * real + imag * imag

def norm_1(real, imag):
    r0 = real
    r1 = imag

    a = r0 * r0
    b = r1 * r1
    r0 = a + b

    return r0

def norm_2(real, imag):
    r0 = real
    r1 = imag

    r0 = r0 * r0
    r1 = r1 * r1
    r0 = r0 + r1

    return r0


for real in test_numbers:
    for imag in test_numbers:
        spec = norm_spec(real, imag)
        result_1 = norm_1(real, imag)
        result_2 = norm_2(real, imag)
        assert spec == result_1 == result_2


def mul_spec(a_real, a_imag, b_real, b_imag):
    real = a_real * b_real - a_imag * b_imag
    imag = a_imag * b_real + a_real * b_imag
    return real, imag

def mul_1(a_real, a_imag, b_real, b_imag):
    a = a_real
    b = a_imag
    c = b_real
    d = b_imag

    e = a * c
    f = b * d
    g = b * c
    h = a * d
    i = e - f
    j = g + h

    return i, j

def mul_2(a_real, a_imag, b_real, b_imag):
    r0 = a_real
    r1 = a_imag
    r2 = b_real
    r3 = b_imag

    e = r0 * r2
    f = r1 * r3
    g = r1 * r2
    h = r0 * r3
    r0 = e - f
    r1 = g + h

    return r0, r1

def mul_3(a_real, a_imag, b_real, b_imag):
    r0 = a_real
    r1 = a_imag
    r2 = b_real
    r3 = b_imag

    stash = [0] * 4

    stash[0] = r0
    stash[1] = r1
    r0 = r0 * r2
    r1 = r1 * r3
    stash[2] = r0
    stash[3] = r1
    r0 = stash[0]
    r1 = stash[1]
    r2 = r1 * r2
    r3 = r0 * r3
    r0 = stash[2]
    r1 = stash[3]
    r0 = r0 - r1
    r1 = r2 + r3

    return r0, r1

for a_real in test_numbers:
    for a_imag in test_numbers:
        for b_real in test_numbers:
            for b_imag in test_numbers:
                spec = mul_spec(a_real, a_imag, b_real, b_imag)
                result_1 = mul_1(a_real, a_imag, b_real, b_imag)
                result_2 = mul_2(a_real, a_imag, b_real, b_imag)
                result_3 = mul_3(a_real, a_imag, b_real, b_imag)
                assert spec == result_1 == result_2 == result_3
