
function Clifford(dx, x, p, n)
    dx[1] = sin(p[1] * x[2]) + p[3] * cos(p[1] * x[1])
    dx[2] = sin(p[2] * x[1]) + p[4] * cos(p[2] * x[2])
    return
end

function Chor1(dx, x, p, n)
    a, b, c, d = p
    dx[1] = sin(a * x[2])^2 + c * cos(a * x[1])
    dx[2] = sin(b * x[1]) + d * cos(b * x[2])^2
end

function Chor2(dx, x, p, n)
    a, b, c, d = p
    dx[1] = sin(a * x[2]) + c * cos(a * x[1])
    dx[2] = d * cos(b * x[1]) + sin(b * x[2])
end

function De_Jong(dx, x, p, n)
    a, b, c, d = p
    dx[1] = sin(a * x[2]) - cos(b * x[1])
    dx[2] = sin(c * x[1]) - cos(d * x[2])
    return
end

function Svensson(dx, x, p, n)
    a, b, c, d = p
    dx[1] = d * sin(a * x[1]) - sin(b * x[2])
    dx[2] = c * cos(a * x[1]) + cos(b * x[2])
end

function Bedhead(dx, x, p, n)
    a, b = p
    dx[1] = sin(x[1]*x[2]/b)*x[2] + cos(a*x[1]-x[2])
    dx[2] = x[1] + sin(x[2])/b
end

function Fractal_Dream(dx, x, p, n)
    a, b, c, d = p
    dx[1] = sin(x[2]*b)+c*sin(x[1]*b)
    dx[2] = sin(x[1]*a)+d*sin(x[2]*a)
    return
end

function Hopalong1(dx, x, p, n)
    a, b, c = p
    dx[1] = x[2] - √(abs(b * x[1] - c)) * sign(x[1])
    dx[2] = a - x[1]
    return
end

function G(x, μ)
    return μ * x + 2 * (1 - μ) * x^2 / (1.0 + x^2)
end

function Gumowski_Mira(dx, x, p, n)
    a, b, μ = p
    dx[1] = x[2] + a*(1 - b*x[2]^2)*x[2]  +  G(x[1], μ)
    dx[2] = -x[1] + G(dx[1], μ)
    return
end

function Symmetric_Icon(dx, x, p, n)
    a, b, g, om, l, d = p
    zzbar = x[1]*x[1] + x[2]*x[2]
    p = a*zzbar + l
    zreal, zimag = x[1], x[2]
    
    for i in range(1, d-1)
        za = zreal * x[1] - zimag * x[2]
        zb = zimag * x[1] + zreal * x[2]
        zreal, zimag = za, zb
    end
    
    zn = x[1]*zreal - x[2]*zimag
    p += b*zn
    
    dx[1] = p*x[1] + g*zreal - om*x[2]
    dx[2] = p*x[2] - g*zimag + om*x[1]
    return
end



