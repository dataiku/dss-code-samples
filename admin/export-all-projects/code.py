import dataiku

def export_all_projects(client=None, target_dir=None, chunk_size=512):
    for p in client.list_projects():
        p_key = p["projectKey"]
        export_name = p_key + ".zip"
        print("Exporting {}...".format(p_key))
        project = client.get_project(p_key)
        with project.get_export_stream() as s:
            target = os.path.join(target_dir, export_name)
            file_handle = open(target, "wb")
            for chunk in s.stream(chunk_size):
                file_handle.write(chunk)
        print("Export succeded, check output at {}".format(target))


