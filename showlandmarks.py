#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : nicolas Loiseau--Witon
# Laboratory : CREATIS, Lyon
import math

import vtk
import pandas as pd
from pathlib import Path
from nibabel import affines
import numpy.linalg as npl
import nibabel as nib
import numpy as np
import SimpleITK as sitk


def jp(x, y):
	return Path.joinpath(x, y)


def get_reader(file_name):
	# 1. Source -Reader
	# reader=vtk.vtkJPEGReader()
	reader = vtk.vtkNIFTIImageReader()
	reader.SetFileName(file_name.as_posix())
	reader.Update()
	return reader


def set_colors_volprop_opacity():
	# 2. Filter --&gt; Setting the color mapper, Opacity for VolumeProperty
	color_func = vtk.vtkColorTransferFunction()

	color_func.AddRGBPoint(-2048.0, 0., 0., 0.)
	color_func.AddRGBPoint(136.47, 0./255., 0./255., 0./255.)
	color_func.AddRGBPoint(159.22, 41./255., 41./255., 41./255.)
	color_func.AddRGBPoint(318.43, 195./255., 195./255., 195./255.)
	color_func.AddRGBPoint(478.69, 255./255., 255./255., 255./255.)
	color_func.AddRGBPoint(3661.0, 0., 0., 0.)


	# color_func.AddRGBPoint(-2048.0, 0.8, 0.8, 0.8)
	# color_func.AddRGBPoint(136.47, 0., 0., 0.)
	# color_func.AddRGBPoint(159.0, 0., 0., 0.)
	# color_func.AddRGBPoint(318.0, 0., 0., 0.)
	# color_func.AddRGBPoint(478.0, 0., 0., 0.)

	opacity = vtk.vtkPiecewiseFunction()
	# opacity.AddPoint(1500, 0.,0., 0.0)
	# opacity.AddPoint(2, 0.0, 0.0, 0.0)
	# opacity.AddPoint(100, 0.0)
	# opacity.AddPoint(155, 0.2)
	opacity.AddPoint(-2048.0, 0.)
	opacity.AddPoint(136.47, 0.)
	opacity.AddPoint(159.22, 0.26)
	opacity.AddPoint(318.43, 0.57)
	opacity.AddPoint(478.69, 0.78)
	opacity.AddPoint(3661.0, 1.)

	# The previous two classes stored properties and we want to apply
	# these properties to the volume we want to render,
	# we have to store them in a class that stores volume properties.
	volume_property = vtk.vtkVolumeProperty()
	# set the color for volumes
	volume_property.SetColor(color_func)
	# To add black as background of Volume
	volume_property.SetScalarOpacity(opacity)
	volume_property.SetInterpolationTypeToLinear()
	volume_property.SetIndependentComponents(5)
	return color_func, opacity, volume_property


def afficher_point(point, colors, ren, color: str='blue'):
	sphereSource = vtk.vtkSphereSource()
	sphereSource.SetCenter(*point)
	sphereSource.SetRadius(10.0)
	# Make the surface smooth.
	sphereSource.SetPhiResolution(200)
	sphereSource.SetThetaResolution(200)

	mapperpt = vtk.vtkPolyDataMapper()
	mapperpt.SetInputConnection(sphereSource.GetOutputPort())

	actorpt = vtk.vtkActor()
	actorpt.SetMapper(mapperpt)
	actorpt.GetProperty().SetColor(colors.GetColor3d(color))

	ren.AddActor(actorpt)

def png_2vols_lands(
		f_vols,
		f_lands: list= None,
		max_im_perline=5,
		max_im_percol=5,
		png_o=None,
		disp=False,
		disp_line=True,
		win_name='volume'):
	"""

	Parameters
	----------
	f_vol_1
	f_vol_2
	f_land_1
	f_land_2
	png_o
	disp_line
	png_o => un fichier Path('.png')
	disp

	Returns
	-------
	"""

	nb_image = len(f_vols)
	maxi_xy = np.array([0, 0, 0])
	if nb_image > 1:
		for f_vol in f_vols:
			maxi_xy = np.maximum(nib.load(f_vol).shape, maxi_xy)

	color_func, opacity, volume_property = set_colors_volprop_opacity()
	colors = vtk.vtkNamedColors()

	ren = vtk.vtkRenderer()
	# No need to set by default it is black
	ren.SetBackground(255, 255, 255)
	# TODO gerer le spacing pour le placement (pour le moment *1.5)
	spaci = 1.5
	for ind, f_vol in enumerate(f_vols):
		print(f_vol, ind)
		reader = get_reader(f_vol)
		spaci = reader.GetDataSpacing()

		# Ray cast function know how to render the data
		volume_mapper = vtk.vtkOpenGLGPUVolumeRayCastMapper()
		volume_mapper.SetInputConnection(reader.GetOutputPort())
		volume_mapper.SetBlendModeToMaximumIntensity()

		volume = vtk.vtkVolume()
		volume.SetMapper(volume_mapper)
		volume.SetProperty(volume_property)
		print(ind, max_im_perline, maxi_xy)
		volume.SetPosition((ind%max_im_perline)*maxi_xy[0] * spaci[0],
							0,
						   math.floor(ind/max_im_perline)*maxi_xy[2] * spaci[2])
		ren.AddVolume(volume)

	ren_win = vtk.vtkRenderWindow()
	if disp is False:
		ren_win.SetOffScreenRendering(1)
	ren_win.AddRenderer(ren)
	ren_win.SetSize(900, 900)
	ren_win.SetWindowName(win_name)

	if f_lands != None:
		for ind, pts in enumerate(f_lands):
			# pts = pd.read_csv(land_f).to_numpy()[:, 1:4]

			im_1 = sitk.ReadImage(f_vols[ind].as_posix(),
							  sitk.sitkFloat32, 'NiftiImageIO')
			ori = np.array(im_1.GetOrigin())

			# TODO gerer les orientations
			ori[1] = -ori[1]
			ori[2] = 0.

			for pt in pts:
				pt = pt-ori
				# pt = [p for p in pt]
				# pt = np.array(im_1.TransformPhysicalPointToIndex(pt))
				# pt[0] += ((ind % max_im_perline) * maxi_xy[0])
				# pt[2] += (math.floor(ind / max_im_perline) * maxi_xy[2] )
				# pt = [int(p) for p in pt]
				# pt = im_1.TransformIndexToPhysicalPoint(pt)
				afficher_point(pt, colors, ren)

	if disp_line is True:
		for ii in range(1, len(f_lands)):
			pts_0 = f_lands[ii-1]
			pts_1 = f_lands[ii]
			maxi = max(len(pts_0), len(pts_1))
			for iii in range(maxi):
				p0 = pts_0[iii]
				p0 = np.array(im_1.TransformPhysicalPointToIndex(p0))
				p0[0] += ((ii-1 % max_im_perline) * maxi_xy[0])
				p0[2] += (math.floor(ii-1 / max_im_perline) * maxi_xy[2])
				p0 = [int(p) for p in p0]
				p0 = im_1.TransformIndexToPhysicalPoint(p0)

				p1 = pts_1[iii]
				p1 = np.array(im_1.TransformPhysicalPointToIndex(p1))
				p1[0] += ((ii % max_im_perline) * maxi_xy[0])
				p1[2] += (math.floor(ii / max_im_perline) * maxi_xy[2])
				p1 = [int(p) for p in p1]
				p1 = im_1.TransformIndexToPhysicalPoint(p1)


				line_src = vtk.vtkLineSource()
				line_src.SetPoint1(p0)
				line_src.SetPoint2(p1)

				# Visualize
				line_color2 = vtk.vtkNamedColors()

				line_map2 = vtk.vtkPolyDataMapper()
				line_map2.SetInputConnection(line_src.GetOutputPort())
				line_act2 = vtk.vtkActor()
				line_act2.SetMapper(line_map2)
				line_act2.GetProperty().SetLineWidth(0.5)
				line_act2.GetProperty().SetColor(line_color2.GetColor3d("green"))

				ren.AddActor(line_act2)

	a_camera = vtk.vtkCamera()
	a_camera.SetViewUp(0, 0, 1)
	a_camera.SetPosition(0, 1, 0)
	a_camera.SetFocalPoint(0, 0, 0)
	a_camera.ComputeViewPlaneNormal()
	a_camera.Azimuth(0.0)
	a_camera.Elevation(0.0)
	ren.SetActiveCamera(a_camera)
	ren.ResetCamera()


	if disp is True:
		interactor = vtk.vtkRenderWindowInteractor()
		interactor.SetRenderWindow(ren_win)
		# interactor.ResetCamera()

		style = vtk.vtkInteractorStyleTrackballCamera()
		interactor.SetInteractorStyle(style)
		interactor.Initialize()
		interactor.Start()
	ren_win.Render()

	if png_o is not None:
		w2if = vtk.vtkWindowToImageFilter()
		w2if.SetInput(ren_win)
		w2if.SetInputBufferTypeToRGB()
		w2if.ReadFrontBufferOff()
		w2if.Update()

		writer = vtk.vtkPNGWriter()
		writer.SetFileName(png_o.as_posix())
		writer.SetInputConnection(w2if.GetOutputPort())
		writer.Write()


def open_rand(f_lan, f_lan1, n_rand=100):
	a = pd.read_csv(f_lan, header=None).to_numpy()[:, 0:3]
	b = pd.read_csv(f_lan1, header=None).to_numpy()[:, 0:3]
	import random
	n_max = min(a.shape[0], b.shape[0])
	c = random.sample(range(1, n_max), n_rand)
	a = a[c]
	b = b[c]
	# a[:,0] = -a[:,0]
	# a[:,1] = -a[:,1]
	# b[:,0] = -b[:,0]
	# b[:,1] = -b[:,1]
	return a, b

if __name__ == '__main__':
	import SimpleITK as sitk
	import numpy as np
	from pathlib import Path


	# vols_f = Path(f'/home/loiseau/Data/DATASETEST/transforms_vol/100/')
	# vols_f = list(vols_f.glob('*.nii.gz'))
	# vols_f = sorted(vols_f)

	# lands_f = Path(f'/home/loiseau/Bureau/Doctorat/'
	# 			   f'Test_detection_superpoint/tracker_outputs')
	# lands_f = list(lands_f.glob('*.csv.gz'))
	# lands_f = sorted(lands_f)
	# lands = [ pd.read_csv(land_f, header=None).to_numpy()[:,:3]
	# 		  for land_f in lands_f]

	lands_f = Path(f'/home/loiseau/Data/Landmarks_LiTS/Nicolas/points_4.fcsv')
	lands = [ pd.read_csv(lands_f, skiprows=3, header=None).to_numpy()[:,1:4]]
	
	lands[0][:, 0] = -lands[0][:, 0]
	lands[0][:, 1] = -lands[0][:, 1]
	lands[0][:, 2] = -lands[0][:, 2]

	vols_f = Path(f'/run/media/loiseau/HDD/Data/LiTS/Volumes/volume-4.nii.gz')
	vols_f = [vols_f]


	png_2vols_lands(
		vols_f,
		f_lands=lands,
		disp=True,
		disp_line=False)
