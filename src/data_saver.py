import os
import vtk
import numpy as np

def save_voxels_with_occupancy(
    file_path: str,
    voxel_points: np.ndarray,
    occupancy: np.ndarray
    ) -> None:
    """Save the voxel points with their occupancy to a file.

    Parameters
    ----------
    file_path : str
        The path to the file to save the voxel points to.
    voxel_points : ndarray
        The points of the voxel grid in homogeneous world coordinates.
    occupancy : ndarray
        The number of image masks each voxel point is inside.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w') as f:
        f.write("x, y, z, occ\n")
        for occ, p in zip(occupancy, voxel_points.T[:, :-1]):
            f.write(", ".join(p.astype(str)) + ", " + str(occ) + "\n")

def save_voxels_as_rectilinear_grid(
    file_path: str,
    voxel_points: np.ndarray,
    occupancy: np.ndarray,
    mesh_grid_size: int
    ) -> None:
    """
    Save the voxel points as a rectilinear grid for paraview visualization.
    
    Parameters 
    ----------
    file_path : str
        The path to the file to save the rectilinear grid to.
    voxel_points : ndarray
        The points of the voxel grid in homogeneous world coordinates.
    occupancy : ndarray
        The number of image masks each voxel point is inside.
    mesh_grid_size : int
        The number of points in each dimension of the voxel grid.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Get the (mesh_grid_size, mesh_grid_size, mesh_grid_size) coordinates
    # of the voxel grid. Map the coordinates as the ones of paraview 
    # (x -> y; y -> z; z -> x).
    y = voxel_points[0, :mesh_grid_size*mesh_grid_size:mesh_grid_size]
    z = voxel_points[1, ::mesh_grid_size*mesh_grid_size]
    x = voxel_points[2, :mesh_grid_size]

    x_coords = vtk.vtkFloatArray()
    for i in x:
        x_coords.InsertNextValue(i)

    y_coords = vtk.vtkFloatArray()
    for i in y:
        y_coords.InsertNextValue(i)

    z_coords = vtk.vtkFloatArray()
    for i in z:
        z_coords.InsertNextValue(i)

    values = vtk.vtkFloatArray()
    for i in occupancy:
        values.InsertNextValue(i)

    rgrid = vtk.vtkRectilinearGrid()
    rgrid.SetDimensions(len(x), len(y), len(z))
    rgrid.SetXCoordinates(x_coords)
    rgrid.SetYCoordinates(y_coords)
    rgrid.SetZCoordinates(z_coords)
    rgrid.GetPointData().SetScalars(values)

    writer = vtk.vtkXMLRectilinearGridWriter()
    writer.SetFileName(file_path)
    writer.SetInputData(rgrid)
    writer.Write()
