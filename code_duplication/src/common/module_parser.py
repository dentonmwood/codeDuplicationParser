import ast
from os import listdir, path
from os.path import isdir, isfile
from .TreeNode import TreeNode
from collections import deque
from .repo_cloner import clone_root_dir


def _read_whole_file(file_path):
    """
    Read a text file into a single string.
    Assumes UTF-8 encoding.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def _read_ast_from_file(file_path):
    return ast.parse(_read_whole_file(file_path))


def _get_tree_from_file(file_path):
    module_node = _read_ast_from_file(file_path)
    file_rel_path = file_path.replace(clone_root_dir, "...")
    return TreeNode(module_node, file_rel_path)


def _recursive_listdir_py(directory):
    """
    Returns relative paths of all *.py files in the specified directory.
    If the provided argument is not a valid directory,
    an internal exception will be thrown by Python.
    That exception will most likely be NotImplementedError.
    """

    files = []

    for item in listdir(directory):
        fullpath = path.join(directory, item)

        if isfile(fullpath) and item.endswith("py"):
            files.append(fullpath)
        elif isdir(fullpath):
            files.extend(_recursive_listdir_py(fullpath))

    return files


def _flatten_module_nodes(module):
    module_nodes = []
    node_queue = deque([module])

    while node_queue:
        n = node_queue.popleft()

        # Set this node's self-index.
        n.index = len(module_nodes)

        # Add this node's index to the list of
        # children of its parent if it has any.
        if n.parent_index is not None:
            module_nodes[n.parent_index].child_indices.append(n.index)

        # Set this node's children's parent index to this node's index.
        for c in n.children:
            c.parent_index = n.index

        # Add this node's children to the queue.
        node_queue.extend(n.children)

        # Add this node to the list of already visited nodes.
        module_nodes.append(n)

    return module_nodes


def get_modules_from_dir(directory):
    """
    Finds all *.py files in the directory recursively and
    returns a module for each one of them wrapped in TreeNode.
    """

    return [_flatten_module_nodes(_get_tree_from_file(f))
            for f in _recursive_listdir_py(directory)]
