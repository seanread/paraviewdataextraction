from paraview.simple import * # NOQA
import numpy as np


class wssCs(object):

    def __init__(self, dataset):

        self.dataset = dataset

        self.description = 'set of functions for working with wall shear stress'

        self. author = 'Sean Read'


class ex(wssCs):

    def __init__(self, dataset):

        super(ex, self).__init__(dataset)

    def clipper(self, sign, clipp, newclip, extract):

        if extract is True:

            ExtractBlock1 = ExtractBlock()

            moblock = {'4': 1,
                       '5': 2,
                       '6': 2,
                       '7': 1,
                       '9': 1}

            ExtractBlock1.BlockIndices = [moblock['%d' % self.dataset]]

        clip = {'co5': [-0.0454, -0.02, 0.0018],  # NC05
                'cn5': [0.03, 0.05, 1],
                'co4': [-0.0455, -0.021, -0.005],  # NC04
                'cn4': [-0.054, 0.033, 1],
                'co6': [-0.0428, -0.0206, 0.0088],  # NC06
                'cn6': [0.214, 0.0287, 0.976],
                'co7': [0.0638, -0.0197, 0.00054],  # NC07
                'cn7': [-0.0102, -0.0587, -0.998],
                'co9': [0.00755, -0.0463, -0.0012],  # NC09
                'cn9': [0, 0.02, 1]}

        if newclip is True:

            Clip1 = Clip(ClipType="Plane")

            Clip1.ClipType = "Plane"

            Clip1 = FindSource('Clip1')

            if sign == '-':

                Clip1.ClipType.Normal = [-clip['cn%d' % self.dataset][i]
                                         for i in range(len(clip['cn%d' % self.dataset]))] # NOQA

            else:

                Clip1.ClipType.Normal = clip['cn%d' % self.dataset]

            Clip1.ClipType.Origin = clip['co%d' % self.dataset]

        if clipp is True:

            Clip1 = FindSource('Clip1')

            if sign == '-':

                Clip1.ClipType.Normal = [-clip['cn%d' % self.dataset][i]
                                         for i in range(len(clip['cn%d' % self.dataset]))] # NOQA

            else:

                Clip1.ClipType.Normal = clip['cn%d' % self.dataset]

            Clip1.ClipType.Origin = clip['co%d' % self.dataset]

    def sledge(self):

        Sli = Slice(SliceType="Plane")

        Sli.SliceOffsetValues = [0.0]

        Sli.SliceType.Normal = [1, 0, 0]

        Sli.SliceType = "Plane"

        Sli = FindSource("Slice1")

        IntegrateVariables()

        SetActiveSource(Sli)

        FeatureEdges()

        featureEdges1 = FindSource('FeatureEdges1')

        SetActiveSource(featureEdges1)

        featureEdges1.FeatureEdges = 0

        featureEdges1.NonManifoldEdges = 0

        IntegrateVariables()

        Render()

    def exwssCs(self, clip):
        if clip is False:
            from math import tan, pi

            ExtractBlock1 = ExtractBlock()

            moblock = {'4': 1,
                       '5': 2,
                       '6': 2,
                       '7': 1,
                       '9': 1}

            ExtractBlock1.BlockIndices = [moblock['%d' % self.dataset]]

            self.sledge()

            WSS = {}

            points = {'4': [25, 45, 75],
                      '5': [20, 45, 70],
                      '6': [-17.1, -42.5, -65],
                      '7': [14.5, 36.1, 62],
                      '9': [14.2, 35.8, 64]}

            angles = {'4': [13, 0.008],
                      '5': [35, 0.003],
                      '6': [41, 0.008],
                      '7': [36, 0.015],
                      '9': [27, 0.05]}
            from paraview import numpy_support as ns

            Sli = FindSource('Slice1')

            featureEdges1 = FindSource('FeatureEdges1')

            for i in range(3):

                if i == 2:

                    Sli.SliceType.Origin = [points['%d' % self.dataset][2]*0.001, # NOQa

                                            -angles['%d' % self.dataset][1], 0]

                    if self.dataset == 6:

                        Sli.SliceType.Normal = [1, tan(float(
                            angles['%d' % self.dataset][0])/50*pi/2), 0]

                    else:

                        Sli.SliceType.Normal = [1, -tan(float(
                            angles['%d' % self.dataset][0])/50*pi/2), 0]
                else:
                    Sli.SliceType.Origin = [points['%d' % self.dataset][i]*0.001, 0, 0] # NOQA

                fedge = servermanager.Fetch(featureEdges1)

                rfedge = fedge.GetBlock(0)

                WSS['%d' % i] = []

                WSS['%d' % i].append(ns.vtk_to_numpy(
                    rfedge.GetPointData().GetArray('wall_shear')))

                WSS['%d' % i].append(ns.vtk_to_numpy(rfedge.GetPointData().GetArray('y_coordinate')))  # NOQA

                WSS['%d' % i].append(ns.vtk_to_numpy(rfedge.GetPointData().GetArray('z_coordinate')))  # NOQA

        elif clip is True:

            from math import tan, pi
            self.clipper('+', False, True, True)
            self.sledge()

            WSS = {}

            points = {'4': [13.8, 34.9, 75],
                      '5': [15.44, 38.5, 70],
                      '6': [17.1, 42.5, 65],
                      '7': [14.5, 36.1, 62],
                      '9': [14.2, 35.8, 64]}

            angles = {'4': [13, 0.008],
                      '5': [35, 0.003],
                      '6': [41, 0.008],
                      '7': [36, 0.015],
                      '9': [27, 0.05]}
            from paraview import numpy_support as ns

            Sli = FindSource('Slice1')

            featureEdges1 = FindSource('FeatureEdges1')

            for i in range(2):

                self.clipper('+', True, False, False)

                Sli.SliceType.Origin = [points['%d' % self.dataset][i]*0.001, 0, 0] # NOQA

                fedge = servermanager.Fetch(featureEdges1)

                rfedge = fedge.GetBlock(0)

                WSS['%dleft' % i] = []

                WSS['%dleft' % i].append(ns.vtk_to_numpy(
                    rfedge.GetPointData().GetArray('wall_shear')))

                WSS['%dleft' % i].append(ns.vtk_to_numpy(rfedge.GetPointData().GetArray('y_coordinate')))  # NOQA

                WSS['%dleft' % i].append(ns.vtk_to_numpy(rfedge.GetPointData().GetArray('z_coordinate')))  # NOQA

                self.clipper('-', True, False, False)

                featureEdges1 = FindSource('FeatureEdges1')

                fedge = servermanager.Fetch(featureEdges1)

                rfedge = fedge.GetBlock(0)

                WSS['%dright' % i] = []

                WSS['%dright' % i].append(ns.vtk_to_numpy(rfedge.GetPointData().GetArray('wall_shear')))  # NOQA

                WSS['%dright' % i].append(ns.vtk_to_numpy(rfedge.GetPointData().GetArray('y_coordinate')))  # NOQA

                WSS['%dright' % i].append(ns.vtk_to_numpy(rfedge.GetPointData().GetArray('z_coordinate')))  # NOQA

            integrateVariables2 = FindSource('integrateVariables2')
            # destroy integrateVariables2
            Delete(integrateVariables2)
            del integrateVariables2

            # destroy featureEdges1
            Delete(featureEdges1)
            del featureEdges1

            integrateVariables1 = FindSource('IntegrateVariables1')
            # destroy integrateVariables1
            Delete(integrateVariables1)
            del integrateVariables1

            slice1 = FindSource('Slice1')
            # destroy slice1
            Delete(slice1)
            del slice1

            clip1 = FindSource('Clip1')
            # destroy clip1
            Delete(clip1)
            del clip1

            # find source
            nCencas = FindSource('NC0%d.encas' % self.dataset)

            # set active source
            SetActiveSource(nCencas)

            extractBlock1 = FindSource('ExtractBlock1')

            # destroy extractBlock1
            Delete(extractBlock1)
            del extractBlock1

            sledge()

            Sli = FindSource('Slice1')

            featureEdges1 = FindSource('FeatureEdges1')

            Sli.SliceType.Origin = [points['%d' % self.dataset][2]*0.001,

                                    -angles['%d' % self.dataset][1], 0]

            Sli.SliceType.Normal = [1, -tan(float(
                angles['%d' % self.dataset][0])/50*pi/2), 0]

            fedge = servermanager.Fetch(featureEdges1)

            rfedge = fedge.GetBlock(0)

            WSS['2'] = []

            WSS['2'].append(ns.vtk_to_numpy(
                rfedge.GetPointData().GetArray('wall_shear')))

            WSS['2'].append(ns.vtk_to_numpy(rfedge.GetPointData().GetArray('y_coordinate')))  # NOQA

            WSS['2'].append(ns.vtk_to_numpy(rfedge.GetPointData().GetArray('z_coordinate')))  # NOQA

        return(WSS)

    def wssCs2f(self, clip, filename):

        import cPickle as pickle
        y = self.exwssCs(clip)
        with open(filename, 'wb') as rrr:

            pickle.dump(y, rrr, 2)
        return y


class pplot(wssCs):

    def __init__(self, dataset, datadic):

        super(pplot, self).__init__(dataset)

        self.datadic = datadic

    def reorder(self, slice):
        """put points in order"""

        x = np.array(self.datadic[slice]).T

        r = np.array([x[0, :]])
        l = np.array([x[0, :]])
        diff = 100
        for i in range(len(x)):
            for i in x[:, 0:3]:
                ndiff = ((r[0, 1]-i[1])**2 + (r[0, 2]-i[2])**2)**0.5
                if ndiff < diff:
                    diff = ndiff
                    p = np.array([i])
            diff = 100
            x = np.delete(x, np.where((x == p).all(1))[0][0], 0)
            r = p
            l = np.append(l, p, axis=0)
        return l

    def separate(self, slice):
        """ separate cavities """

        IN = self.reorder(slice)

        diff = 0

        for i in range(1, len(IN)):
            ndiff = ((IN[i, 1]-IN[(i-1), 1])**2 + (IN[i, 2] - IN[i-1, 2])**2)**0.5 # NOQA
            if ndiff > diff:
                diff = ndiff
                loc = i
        IN1 = IN[:loc-1, :]
        IN2 = IN[loc:, :]

        if slice == '1':
            if self.dataset in [5, 6, 9]:
                return [IN2, IN1]
            else:
                return [IN1, IN2]
        elif slice == '0':
            if self.dataset == 5:
                return [IN2, IN1]
            else:
                return [IN1, IN2]

    def ymax(self, slice, separate, side):
        """reorient dataset so that start is at ymax"""
        if separate is True:
            l = self.separate(slice)

        else:
            l = self.reorder(slice)

        if separate is True:
            l1 = []
            for grr in range(len(l)):

                reg = -100

                for i in np.array(l[grr][:, 1]):
                    if i > reg:
                        reg = i
        # Check for consistency in direction of array for simple two cavity
        # cases

                if len(l) == 2:
                    x = l[grr][:, 2]
                    g = np.where(np.array(l[grr][:, 1]) ==
                                 np.array([reg]))[0][0]

                    if grr == 0:
                        cond = x[g] < x[g-1]
                    else:
                        cond = x[g] > x[g-1]

                    if cond:
                        l1.append(np.append(l[grr][g: len(l[grr]), :],
                                            l[grr][: g-1, :], axis=0))
                    else:
                        l1.append(np.flipud(np.append(l[grr][g: len(l[grr]), :],
                                            l[grr][: g-1, :], axis=0)))
                else:
                    l1.append(np.append(l[grr][g: len(l[grr]), :],
                                        l[grr][: g-1, :], axis=0))

# returning to function if separate == False:

        else:

            reg = -100

            for i in np.array(l[:, 1]):
                if i > reg:
                    reg = i
            x = l[:, 2]
            g = np.where(np.array(l[:, 1]) == np.array([reg]))[0][0]

            if side == 'l':
                cond = x[g] < x[g-1]
            else:
                cond = x[g] > x[g-1]

            if cond:
                l1 = np.append(l[g:len(l), :],
                               l[:g-1, :], axis=0)
            else:
                l1 = np.flipud(np.append(l[g:len(l), :],
                               l[:g-1, :], axis=0))

        return l1

    def length(self, slice, separate, side='l'):
        """create a list defining the accumulated distance
        of each point and append to array""" # NOQA

        r = self.ymax(slice, separate, side)

        if separate is True:
            l1 = [[0], [0]]

            for l in range(len(r)):

                for i in range(len(r[l]) - 1):
                    l1[l].append(((r[l][i, 1] - r[l][i - 1, 1])**2 + (r[l][i, 2] - r[l][i - 1, 2])**2)**0.5 + l1[l][i]) # NOQA

            out = [np.append(r[i], np.array([l1[i]]).T, 1)
                   for i in range(len(r))]

        else:

            l1 = [0]

            for i in range(len(r) - 1):
                l1.append(((r[i, 1] - r[i - 1, 1])**2 + (r[i, 2] - r[i - 1, 2])**2)**0.5 + l1[i]) # NOQA
            out = np.append(r, np.array([l1]).T, 1)
        return out

    def load(self, slice):
        import cPickle as pickle
        lis = []
        for i in ['4', '5', '6', '7', '9', '9lr', '5lr']:
            with open('wssCs/NC0' + i + '.pickle', 'rb') as lll:
                lis.append(pickle.load(lll))
        lom = [4, 5, 6, 7, 9]
        name = ['NC0%d' % rrr for rrr in lom]
        dic = {}
        for i in range(len(name)):
            dic[name[i]] = pplot(lom[i], lis[i])
        lisss = [dic[var].length('1', True) for var in name]

        if slice == '1':
            exc = [[], []]
            dic['9alt'] = self.pplot(5, lis[5])
            dic['5alt'] = self.pplot(9, lis[6])
            r = [5, 9]
            for i in range(2):
                for l in ['left', 'right']:
                    exc[i].append(dic['%dalt' % r[i]].length('1'+l, False))
            lisss = [lisss[0], exc[0], lisss[2], lisss[3], exc[1]]

        temp = lisss[4]
        new = []
        for r in range(len(temp)):
            new.append(np.flipud(temp[r]))
        temp = lisss[0:4]
        temp.append(new)
        lisss = temp

        return lisss
