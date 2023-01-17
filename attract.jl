using DynamicalSystems
using NCDatasets
using YAML

N = 1e8

include("attractor_functions.jl")

attractors = YAML.load_file("strange_attractors.yml")

for (i, attractor) in enumerate(attractors)
    funcname, cmap, options... = attractor
    @info i funcname cmap options

    x⃗₀ = options[1:2]
    params = options[3:end]

    funcsymbol = Meta.parse(funcname)
    x⃗₀ = convert(Array{Float64,1}, x⃗₀)
    params = convert(Array{Float64,1}, params)

    dsystem = DiscreteDynamicalSystem(eval(funcsymbol), x⃗₀, params)

    global traj = trajectory(dsystem, N)

    @info "Writing to file..."
    ncfile = NCDataset("data/$(i)_$funcname.nc", "c")

    defDim(ncfile,"step", length(traj))

    ncfile.attrib["title"] = "$funcname attractor number $i"
    ncfile.attrib["initial conditions"] = string(params)

    x = defVar(ncfile, "x", Float64, ("step",))
    y = defVar(ncfile, "y", Float64, ("step",))

    x[:] = Matrix(traj)[:,1]
    y[:] = Matrix(traj)[:,2]

    close(ncfile)

#    ncfile = NCDataset("data/$(i)_$funcname.nc", "c")
#    @show ncfile["x"][1:10]
#    close(ncfile)
#    pause

end

