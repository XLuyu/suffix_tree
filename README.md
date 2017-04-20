# suffix_tree
A suffix tree implementation in Python
# Algorithm
Ukkonen E. On-line construction of suffix trees[J]. Algorithmica, 1995, 14(3): 249-260.
https://www.cs.helsinki.fi/u/ukkonen/SuffixT1withFigs.pdf

*Notice: In this paper, the template use 1-based indexing. But here I use 0-based indexing.*

# Visualization (Optional)
This code utilizes graphviz to visualize constructed tree and matching process.
1. Install [graphviz](http://www.graphviz.org/Download..php) and make sure it is in PATH  
*(type "dot -version" in command line/shell to check whether it prints version info)*
2. Install [graphviz python binding](https://pypi.python.org/pypi/graphviz) by `pip install graphviz`
3. In the code, you can call st.plot_tree() to visualize it after construction.  
*The generated `.png` files are in the `visualization` subdirectory"
4. You can also match_pattern_suffix(pattern,visual=True) to generate image files for each step in matching.
*The red node in image indicates current state, the string in the red node indicates matched part on some edge from this node*

#Contact
taoistly@gmail.com
