import dataiku

def delete_orphaned_datasets(client=None, project_key=None, drop_data=False, dry_run=True):
    """Delete datasets that are not linked to any recipe.
    """
    prj = client.get_project(project_key)
    flow = prj.get_flow()
    graph = flow.get_graph()
    cpt = 0
    for name, props in graph.nodes.items():
        if not props["predecessors"] and not props["successors"]:
            print(f"- Deleting {name}...")
            ds = prj.get_dataset(name)
            if not dry_run:
                ds.delete(drop_data=drop_data)
                cpt +=1 
            else:
                print("Dry run: nothing was deleted.")
    print(f"{cpt} datasets deleted.")
