using DynamicalSystems
using NCDatasets
using YAML

N = 1e6

include("attractor_functions.jl")

attractors = YAML.load_file("strange_attractors.yml")

for (i, attractor) in enumerate(attractors)
    funcname, cmap, options... = attractor
    @show i funcname cmap options
    @info ""

    global x⃗₀ = options[1:2]
    global params = options[3:end]

    funcsymbol = Meta.parse(funcname)
    x⃗₀ = convert(Array{Float64,1}, x⃗₀)
    params = convert(Array{Float64,1}, params)

    dsystem = DiscreteDynamicalSystem(eval(funcsymbol), x⃗₀, params)

    traj = trajectory(dsystem, N)

    ncfile = NCDataset("1_Clifford.nc", "c")

    defDim(ncfile,"step", Int(N+1))

    ncfile.attrib["title"] = "Clifford attractor number 1"
    ncfile.attrib["initial conditions"] = string(params)

    x = defVar(ncfile, "x", Float32, ("step",))
    y = defVar(ncfile, "y", Float32, ("step",))

    x = Matrix(traj)[:,1]
    y = Matrix(traj)[:,2]

    close(ncfile)

end
