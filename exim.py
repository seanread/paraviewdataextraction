from paraview.simple import * # NOQA
import numpy as np


class im(object):

    def __init__(self, dataset):

        self.dataset = dataset

        self.description = '''set
        of functions for exporting cross sectional area collages'''

        self. author = 'Sean Read'


class exim(im):

    def __init__(self, dataset):

        super(exim, self).__init__(dataset)

    def eximg(self, res):

        model = self.dataset

        ExtractBlock1 = ExtractBlock()

        moblock = {'4': 1,
                   '5': 2,
                   '6': 2,
                   '7': 1,
                   '9': 1}

        ExtractBlock1.BlockIndices = [moblock['%d' % model]]

        Sli = Slice(SliceType="Plane")

        Sli.SliceOffsetValues = [0.0]

        Sli.SliceType.Normal = [1, 0, 0]

        Sli.SliceType = "Plane"

        Sli = FindSource("Slice1")

        SetActiveSource(Sli)

        FeatureEdges()

        featureEdges1 = FindSource('FeatureEdges1')

        SetActiveSource(featureEdges1)

        featureEdges1.FeatureEdges = 0

        featureEdges1.NonManifoldEdges = 0

        Render()

        cons = {'NC04': 0.08, 'NC04C': 0.01,
                'NC04H': -0.008, 'NC05': 0.08,
                'NC05C': 0.005, 'NC05H': -0.003,
                'NC06': 0.08, 'NC06C': 0.005,
                'NC06H': -0.008, 'NC07': 0.08,
                'NC07C': 0, 'NC07H': -0.015,
                'NC09': 0.08, 'NC09C': 0,
                'NC09H': -0.05}

        Sli = FindSource("Slice1")

        featureEdges1 = FindSource('FeatureEdges1')

        SetActiveSource(Sli)

        from paraview import numpy_support as ns

        img = {}

        img['X'] = []

        img['Y'] = []

        img['Z'] = []

        model = 'NC0%d' % model

        for x in range(res):

            if model == 'NC06':

                Sli.SliceType.Origin = [
                    -x*cons[model]/res - cons[model+'C'], 0, 0]

            else:

                Sli.SliceType.Origin = [
                    x*cons[model]/res + cons[model+'C'], 0, 0]

            img['X'].append(x*cons[model]*1000/res)

            fedge = servermanager.Fetch(featureEdges1)

            rfedge = fedge.GetBlock(0)

            img['Y'].append(ns.vtk_to_numpy(
                rfedge.GetPointData().GetArray('y_coordinate')))

            img['Z'].append(
                ns.vtk_to_numpy(rfedge.GetPointData()
                                .GetArray('z_coordinate')))

        return img

    def im2f(self, res, filename):

        import cPickle as pickle
        y = self.eximg(res)
        with open(filename, 'wb') as rrr:

            pickle.dump(y, rrr, 2)
        return y


class pplot(im):

    def __init__(self, dataset, datadic):

        import cPickle as pickle

        super(pplot, self).__init__(dataset)

        with open(datadic, 'rb') as data:

            self.datadic = pickle.load(data)

    def __str__(self):
        return(str(self.datadic))

    def getdic(self):
        return self.datadic

    def reorder(self, slice):
        """put points in order"""
        diff = 100
        loc = [list(self.datadic['Y'][slice]), list(self.datadic['Z'][slice])]
        r = [loc[0][0], loc[1][0]]
        l = [[loc[0][0], loc[1][0]]]
        for i in range(len(loc[0])):
            for ff in range(len(loc[0])):
                ndiff = ((r[0]-loc[0][ff])**2 + (r[1]-loc[1][ff])**2)**0.5
                if ndiff < diff:
                    diff = ndiff
                    p = [loc[0][ff], loc[1][ff]]
                    lo = ff
            diff = 100
            for rrr in [0, 1]:
                loc[rrr].pop(lo)
            r = p
            l.append(p)
        l = np.array(l)
        return l

    def separate(self, slice, res=0.004):
        """ separate cavities """

        IN = self.reorder(slice)

        loc = [0]

        for i in range(1, len(IN)):
            diff = ((IN[i, 0]-IN[i-1, 0])**2 +
                    (IN[i, 1] - IN[i-1, 1])**2)**0.5
            if diff > res:
                loc.append(i)
        loc.append(len(IN))
        return [IN[loc[i-1]:loc[i], :] for i in range(1, len(loc))]
