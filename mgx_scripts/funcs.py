def do_distance_measures(mesh, types):
    """
    allow user to input cell based axes for measures of distance within a mesh
    :param mesh: string denoting path to mesh to be used
    :param types: list of strings, which axes to measure
    :return: none
    """

    return

def do_intra_measures(mesh):
    """
    conduct all single mesh measures, then export attribute map to csv
    :param mesh:
    :return:
    """
    # load mesh
    Process.Mesh__System__Load(os.path.join(file_path, 'meshes', mesh), 'no', 'no', '0')
    Process.Stack__System__Set_Current_Stack('Main', '0')

    # run desired processes
    Process.Mesh__Heat_Map__Measures__Geometry__Area()
    Process.Mesh__Heat_Map__Measures__Geometry__Aspect_Ratio()
    Process.Mesh__Heat_Map__Measures__Geometry__Average_Radius()
                                                            # min or max, direct junctions (yes) or also neighbors (no)
    Process.Mesh__Heat_Map__Measures__Geometry__Junction_Distance('Min', 'No')
    # todo check that it will measure and save both as attributes
    Process.Mesh__Heat_Map__Measures__Geometry__Junction_Distance('Max', 'No')
    Process.Mesh__Heat_Map__Measures__Geometry__Length_Major_Axis()
    Process.Mesh__Heat_Map__Measures__Geometry__Length_Minor_Axis()
    Process.Mesh__Heat_Map__Measures__Geometry__Maximum_Radius()
    Process.Mesh__Heat_Map__Measures__Geometry__Minimum_Radius()
    Process.Mesh__Heat_Map__Measures__Geometry__Neighbors()
    Process.Mesh__Heat_Map__Measures__Geometry__Perimeter()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Circularity()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Largest_Empty_Space()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Lobeyness()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Rectangularity()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Solidarity()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Visibility_Pavement()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Visibility_Stomata()
    Process.Mesh__Heat_Map__Measures__Neighborhood__Area()
    Process.Mesh__Heat_Map__Measures__Neighborhood__Aspect_Ratio()
    Process.Mesh__Heat_Map__Measures__Neighborhood__Neighbors()
    Process.Mesh__Heat_Map__Measures__Neighborhood__Perimeter()
    Process.Mesh__Heat_Map__Measures__Neighborhood__Variability_Radius()
    Process.Mesh__Heat_Map__Measures__Shape__Bending()
    Process.Mesh__Heat_Map__Measures__Shape__Common_Bending()
    Process.Mesh__Heat_Map__Measures__Shape__Common_Neighbors()
    Process.Mesh__Heat_Map__Measures__Shape__Variability_Radius()


    # save the mesh (attributes saved in mesh)
    #                           filename, transform, mesh number
    Process.Mesh__System__Save(mesh, 'no','0')


    return


def do_inter_measures(mesh_0, mesh_1):
    """
    run processes that track changes between meshes
    :param mesh_0: string, filepath of the first mesh (t)
    :param mesh_1: string, filepath of the second mesh (t+1)
    :return: null
    """
    # load meshes
    Process.Mesh__System__Load(os.path.join(file_path, 'meshes', mesh_0), 'no', 'no', '0')
    Process.Mesh__System__Load(os.path.join(file_path, 'meshes', mesh_1), 'no', 'no', '1')
    Process.Stack__System__Set_Current_Stack('Main', '0')

    # set parents active on the alternate mesh
    root = Tk()
    w = Label(root, text="Hello, world!")
    w.pack()

    root.mainloop()

    # run desired processes

    # save the mesh (attributes saved in mesh)
    #                           filename, transform, mesh number
    Process.Mesh__System__Save(mesh, 'no','0')
    Process.Mesh__System__Save(mesh, 'no', '1')

    return

def do_intra_display(mesh):
    """
    save snapshots for all desired measures
    :param mesh: string, filepath of the mesh
    :return: null
    """
    # load meshes
    Process.Mesh__System__Load(os.path.join(file_path, 'meshes', mesh), 'no', 'no', '0')
    Process.Stack__System__Set_Current_Stack('Main', '0')

    # user adjust arrangement


    # take photos

    return

def do_inter_display(mesh_0, mesh_1):
    # load meshes
    Process.Mesh__System__Load(os.path.join(file_path, 'meshes', mesh_0), 'no', 'no', '0')
    Process.Mesh__System__Load(os.path.join(file_path, 'meshes', mesh_1), 'no', 'no', '1')
    Process.Stack__System__Set_Current_Stack('Main', '0')

    # user adjust arrangement

    # take photos

    return