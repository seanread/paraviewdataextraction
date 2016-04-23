from paraview.simple import * # NOQA


class nc(object):
    def __init__(self, model, data=[], ldat=[], res=100, ext='n'):

        self.inf = None

        self.model = model

        self.data = data

        self.ldat = ldat

        self.res = res

        self.ext = ext

    def clipper(self, sign='+', clipp=False, newclip=False, extract=True):

        model = self.model

        if extract is True:

            ExtractBlock1 = ExtractBlock()

            moblock = {'4': 1,
                       '5': 2,
                       '6': 2,
                       '7': 1,
                       '9': 1}

            ExtractBlock1.BlockIndices = [moblock['%d' % model]]

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

                Clip1.ClipType.Normal = [
                    -clip['cn%d' % model][i]
                    for i in range(len(clip['cn%d' % model]))]

            else:

                Clip1.ClipType.Normal = clip['cn%d' % model]

            Clip1.ClipType.Origin = clip['co%d' % model]

        if clipp is True:

            Clip1 = FindSource('Clip1')

            if sign == '-':

                Clip1.ClipType.Normal = [
                    -clip['cn%d' % model][i]
                    for i in range(len(clip['cn%d' % model]))]

            else:

                Clip1.ClipType.Normal = clip['cn%d' % model]

            Clip1.ClipType.Origin = clip['co%d' % model]

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

    def exdat(self):

        from paraview import numpy_support as ns

        # Define relevant constants
        self.clipper()
        self.sledge()
        data = self.data
        model = 'NC0%d' % self.model
        ldat = self.ldat
        res = self.res

        dic = {'X': [], 'Area': [], 'Len': []}

        for i in data:

            dic[i] = []

        for i in ldat:

            dic[i] = []

        cons = {'NC04': 0.065, 'NC04C': 0.01,
                'NC04H': -0.008, 'NC05': 0.065,
                'NC05C': 0.005, 'NC05H': -0.003,
                'NC06': 0.06, 'NC06C': 0.005,
                'NC06H': -0.008, 'NC07': 0.062,
                'NC07C': 0, 'NC07H': -0.015,
                'NC09': 0.064, 'NC09C': 0,
                'NC09H': -0.05}

        Sli = FindSource("Slice1")

        Integra = FindSource("IntegrateVariables1")

        Int = FindSource("IntegrateVariables2")

        SetActiveSource(Sli)

        # Extract data for main cavity

        for x in range(res):

            if model == 'NC06':

                Sli.SliceType.Origin = [
                    -x*cons[model]/res - cons[model+'C'], 0, 0]

            else:

                Sli.SliceType.Origin = [
                    x*cons[model]/res + cons[model+'C'], 0, 0]

            dic['X'].append(x*cons[model]*1000/res)

            intData = servermanager.Fetch(Integra)
            dic['Area'].append(ns.vtk_to_numpy(intData.GetCellData().GetArray('Area'))[0])  # NOQA
            for i in data:
                dic[i].append(ns.vtk_to_numpy(intData.GetPointData().GetArray(i))[0])  # NOQA

            InDat = servermanager.Fetch(Int)

            dic['Len'].append(ns.vtk_to_numpy(InDat.GetCellData().GetArray('Length'))[0])  # NOQA
            for i in ldat:
                dic[i].append(ns.vtk_to_numpy(InDat.GetPointData().GetArray(i))[0])  # NOQA

        self.inf = dic

        if 'y' == self.ext:

            self.exnp()

    def exnp(self):
        '''Extract data for nasopharynx'''

        data = self.data
        model = 'NC0%d' % self.model
        ldat = self.ldat

        from paraview import numpy_support as ns
        from math import tan, pi

        # set origins
        cons = {'NC04': 0.065, 'NC04C': 0.01,
                'NC04H': -0.008, 'NC05': 0.065,
                'NC05C': 0.005, 'NC05H': -0.003,
                'NC06': 0.06, 'NC06C': 0.005,
                'NC06H': -0.008, 'NC07': 0.062,
                'NC07C': 0, 'NC07H': -0.015,
                'NC09': 0.064, 'NC09C': 0,
                'NC09H': -0.05}

        Sli = FindSource("Slice1")

        Integra = FindSource("IntegrateVariables1")

        Int = FindSource("IntegrateVariables2")

        SetActiveSource(Sli)

        if model == 'NC06':

            Sli.SliceType.Origin = [-cons[model] - cons[model+'C'], cons[model+'H'], 0]  # NOQA

        else:

            Sli.SliceType.Origin = [cons[model] + cons[model+'C'], cons[model+'H'], 0]  # NOQA

        # iterate over nasopharynx

        resp = self.res/4

        for x in range(resp):

            if model == 'NC06':

                Sli.SliceType.Normal = [-1, -tan(pi*x/(2*resp)), 0]

            else:

                Sli.SliceType.Normal = [1, -tan(pi*x/(2*resp)), 0]

            intData = servermanager.Fetch(Integra)

            if model == 'NC09':

                self.inf['X'].append(
                    cons[model]*1000 - x*cons[model+'H']*pi*0.05/resp*1000)

            else:

                self.inf['X'].append(
                    cons[model]*1000 - x*cons[model+'H']*pi*0.5/resp*1000)

            self.inf['Area'].append(ns.vtk_to_numpy(
                intData.GetCellData().GetArray('Area'))[0])

            for i in data:
                self.inf[i].append(
                    ns.vtk_to_numpy(intData.GetPointData().GetArray(i))[0])

            InDat = servermanager.Fetch(Int)

            self.inf['Len'].append(ns.vtk_to_numpy(InDat.GetCellData().GetArray('Length'))[0])  # NOQA

            for i in ldat:
                self.inf[i].append(
                    ns.vtk_to_numpy(InDat.GetCellData().GetArray(i))[0])

    def w2f(self, fil):

        import csv
        Newfile = open(fil, 'wb')

        writer = csv.writer(Newfile, delimiter=',')

        writer.writerow([key for key in self.inf])

        for pos in range(0, len(self.inf['X'])):
            x = [self.inf[key][pos] for key in self.inf]
            writer.writerow(x)


def multiload(files, ext):

    import numpy as np
    dic = {}
    for x in files:
        dic[x] = np.genfromtxt(x+ext, delimiter=",")
    return(dic)
