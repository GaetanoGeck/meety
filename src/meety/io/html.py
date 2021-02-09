def unordered_list(entries):
    if entries:
        lis = "\n".join([f"<li>{e}</li>" for e in entries])
        return f"<ul>{lis}</ul>"
    else:
        return ""
