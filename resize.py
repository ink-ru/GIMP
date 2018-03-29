#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from gimpfu import *
# import os

def resize_image(width):
	image = gimp.image_list()[0]
	height = image.height/(image.width/width)
	pdb.gimp_image_scale(image, width, height)

def scale_image(width, bg_color, hght):
	ratio = width/hght
	image = gimp.image_list()[0]

	offx = offy = 0

	current_ratio = float(image.width/image.height)
	new_width = image.width
	new_height = image.height

	if current_ratio != ratio:
		if current_ratio >= ratio:
			new_width = image.width
			new_height = image.width/ratio
			offy = (new_height-image.height)/2
		else:
			new_width = image.height*ratio
			new_height = image.height
			offx = (new_width-image.width)/2

	pdb.gimp_image_resize (image,new_width,new_height,offx,offy) # pdb.gimp_image_resize

	old_background = pdb.gimp_context_get_background()
	# Меняем цвет фона
	pdb.gimp_context_set_background(bg_color)
	# Сводим изображение
	pdb.gimp_image_flatten(image)
	# Возвращаем в исходное состояние цвет фона
	pdb.gimp_context_set_background(old_background)
	# Обновляем изоборажение на дисплее
	pdb.gimp_displays_flush()

def savePNG(image,filename):
	"""Saves composed image to filename"""
	layers = image.layers
	last_layer = len(layers)-1
	try:
		disable=pdb.gimp_image_undo_disable(image)
		pdb.gimp_layer_add_alpha(layers[0])
		pdb.plug_in_colortoalpha(image,image.active_layer,(0,0,0))
		layer = pdb.gimp_image_merge_visible_layers(image, 1)
		enable = pdb.gimp_image_undo_enable(image)
		pdb.file_png_save(image, image.active_layer, filename, filename, 0,9,1,0,0,1,1)
	except Exception as e:
		raise e

def save(image,filename):
	layers = image.layers
	last_layer = len(layers)-1
	try:
		disable = pdb.gimp_image_undo_disable(image)
		layer = pdb.gimp_image_merge_visible_layers(image, 1)
		enable = pdb.gimp_image_undo_enable(image)
		pdb.gimp_file_save(image, image.active_layer, filename, '?')
	except Exception as e:
		raise e

def scale_and_crop_image(width, hght, bg_color, save_flag):
	width = float(width)
	hght = float(hght)

	ratio = width/hght
	image = gimp.image_list()[0] # TODO: do for all images in a loop

	pdb.gimp_context_push()
	pdb.gimp_image_undo_group_start(image)

	pdb.gimp_progress_init("Scaling Image...",None)
	pdb.gimp_context_set_interpolation(INTERPOLATION_LANCZOS) # INTERPOLATION-CUBIC
	
	scale_image(width, bg_color, hght)
	resize_image(width)

	pdb.gimp_image_undo_group_end(image)
	pdb.gimp_context_pop()

	if save_flag == True:
		save(image, pdb.gimp_image_get_filename(image)) # pdb.gimp_image_get_uri(image)
		pdb.gimp_message('Новое изображение сохранено!')
	else:
		pdb.gimp_message('Done!')

	# pdb.gimp_image_clean_all(image)
	# pdb.gimp_display_delete(gimp.Display(image))
	# pdb.gimp_quit(1)

	return


register(
		 "python-fu-resize",
		 "Приводим изображение к нужному размеру",
		 "Меняем размер изображения",
		 "Васин Юрий",
		 "Васин Юрий",
		 "2018",
		 "Resize",
		 "*", # image type
		 [
			(PF_INT, "width", "Требуемая ширина", 695), # (PF_IMAGE, "image", "Исходное изображение", None),
			(PF_INT, "hght", "Требуемая высота", 462),
			(PF_COLOR, "bg_color",  "Цвет фона", (255,255,255)),
			# (PF_FLOAT, "ratio", "Соотношение сторон (3:2)", 1.5),
			(PF_TOGGLE, "save_flag", "Перезаписать изображение", True),
			],
		 [],
		 scale_and_crop_image,
		 menu="<Image>/DoItUp",
		 domain=("gimp20-python", gimp.locale_directory)
)

main()
