import angr
p = angr.Project("./petshop",auto_load_libs=False)
cfg = p.analyses.CFGFast()
cfg.normalize()
for func_node in cfg.functions.values():
    if func_node.name.startswith("__"):
        continue
    else:
        for block in func_node.blocks:             
            block.pp() 
