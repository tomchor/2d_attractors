using DynamicalSystems
using NCDatasets

N = 1e7

function Clifford!(dx, x, p, n)
    dx[1] = sin(p[1] * x[2]) + p[3] * cos(p[1] * x[1])
    dx[2] = sin(p[2] * x[1]) + p[4] * cos(p[2] * x[2])
    return
end

params = [1.782, 2.234, 1.113, 0.1982]
dsystem = DiscreteDynamicalSystem(Clifford!, zeros(2), params)

traj = trajectory(dsystem, N)

ncfile = NCDataset("1_Clifford.nc", "c")

# Define the dimension "lon" and "lat" with the size 100 and 110 resp.
defDim(ncfile,"step", Int(N+1))

ncfile.attrib["title"] = "Clifford attractor number 1"
ncfile.attrib["initial conditions"] = string(params)

# Define the variables temperature
x = defVar(ncfile, "x", Float32, ("step",))
y = defVar(ncfile, "y", Float32, ("step",))

# write a single column
x = Matrix(traj)[:,1]
y = Matrix(traj)[:,2]

close(ncfile)

