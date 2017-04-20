"""
    A suffix tree implementation in Python
    Algorithm:
        Ukkonen E. On-line construction of suffix trees[J]. Algorithmica, 1995, 14(3): 249-260.
        https://www.cs.helsinki.fi/u/ukkonen/SuffixT1withFigs.pdf
        [Notice]
            1. In this paper, the template use 1-based indexing. However, to be pythonic, here we use 0-based indexing.
            2. Variable names follow the definition in the paper.
    Visualization:
        This code utilizes graphviz to visualize constructed tree and matching process.
    Author:
        Luyu (taoistly@gmail.com)
    Date:
        2017-04-18
"""
import collections


class SuffixTree(object):

    def __init__(self, max_template_length=1000000000):
        self.OO = max_template_length
        self.t = ''  # template
        self.tlen = 0  # template length
        self.start_idx = 0
        self.root = {}
        self.falsum = collections.defaultdict(lambda: (-1, 0, self.root))
        self.root['suffix'] = self.falsum
        self.s, self.k = (self.root, 0)  # active point

    def _test_and_split(self, s, (k, p), t):
        if k < p:
            k_, p_, s_ = s[self.t[k]]
            if t == self.t[k_ + p - k]: return (True, s)
            r = {}
            r[self.t[k_ + p - k]] = (k_ + p - k, p_, s_)
            s[self.t[k_]] = (k_, k_ + p - k, r)
            return (False, r)
        else:
            return (t in s or s is self.falsum, s)

    def _canonize(self, s, (k, p)):
        if p == k: return (s, k)
        k_, p_, s_ = s[self.t[k]]
        while p_ - k_ <= p - k:
            k += p_ - k_
            s = s_
            if k == p: break
            k_, p_, s_ = s[self.t[k]]
        return (s, k)

    def _update(self, s, (k, i)):
        oldr = self.root
        end_point, r = self._test_and_split(s, (k, i - 1), self.t[i - 1])
        while not end_point:
            r[self.t[i - 1]] = (i - 1, self.OO, {'idx': self.start_idx})
            if oldr is not self.root: oldr['suffix'] = r
            oldr = r
            s, k = self._canonize(s['suffix'], (k, i - 1))
            self.start_idx += 1
            end_point, r = self._test_and_split(s, (k, i - 1), self.t[i - 1])
        if oldr is not self.root: oldr['suffix'] = s
        return (s, k)

    def append(self, template):
        """ Feed a string to the suffix tree. It will continue the construction based on the existing tree
            Initially, there is only a root in the tree, this method can be invoked more than once.
        """
        self.t += template
        oldlen, self.tlen = self.tlen, len(self.t)
        for i in range(oldlen, self.tlen):
            self.s, self.k = self._update(self.s, (self.k, i + 1))
            self.s, self.k = self._canonize(self.s, (self.k, i + 1))

    def match_pattern_suffix(self, pattern, visual=False):
        """ match a pattern on the suffix tree.
            if visual is true, it will generate .png files for each index in pattern
            return value is the longest suffix of pattern matched to the template
        """
        s, k, p = self.root, 0, 0
        for idx, i in enumerate(pattern):
            while k < p or s is not self.root:
                if k == p and i in s: break
                if k < p and s[pattern[k]][0] + p - k < self.tlen and self.t[s[pattern[k]][0] + p - k] == i: break
                if s is not self.root:
                    s = s['suffix']
                    while k < p and s[pattern[k]][1] - s[pattern[k]][0] <= p - k:
                        s, k = s[pattern[k]][2], k + s[pattern[k]][1] - s[pattern[k]][0]
                else: k += 1
            if k == p and i in s or k < p and s[pattern[k]][0] + p - k < self.tlen and self.t[s[pattern[k]][0] + p - k] == i:
                p += 1
                while k < p and s[pattern[k]][1] - s[pattern[k]][0] <= p - k:
                    s, k = s[pattern[k]][2], k + s[pattern[k]][1] - s[pattern[k]][0]
            if visual: self.plot_tree("pattern" + str(idx), False, {str(id(s)): pattern[k:p]})
        return pattern[k:p]

    def _traverse(self, tree, curnode, labeldict):
        if labeldict and str(id(curnode)) in labeldict:
            tree.node(str(id(curnode)), label=labeldict[str(id(curnode))], style='filled', fillcolor='red')
        else:
            tree.node(str(id(curnode)), label=str(curnode['idx']) if 'idx' in curnode else '')
        for i in curnode:
            if i == 'suffix':
                if curnode['suffix'] is not self.falsum:
                    tree.edge(str(id(curnode)), str(id(curnode['suffix'])), style="dashed")
            elif i != 'idx':
                tree.edge(str(id(curnode)), str(id(curnode[i][2])), label=self.t.__getslice__(*curnode[i][:2]))
                self._traverse(tree, curnode[i][2], labeldict)

    def plot_tree(self, filename="suffix_tree", view=True, labeldict=None):
        """ plot the tree with given filename in "visualization" subdirectory
            if view is True, it will immediately open the file with system default image browser
        """
        from graphviz import Digraph
        tree = Digraph(format='png')
        self._traverse(tree, self.root, labeldict)
        tree.render("visualization/" + filename, view=view)


if __name__ == '__main__':
    st = SuffixTree()
    st.append('AAATGATCATCAACCACAACAGCCAGG$')
    print st.match_pattern_suffix('CATCAACCACAACAGCCAGGTTGTAGGCGA', True)
