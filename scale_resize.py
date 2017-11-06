# -*- coding: utf-8 -*-

from __future__ import division
from gimpfu import *

# https://habrahabr.ru/post/135863/

def resize_image(width):
	image = gimp.image_list()[0]

	if image.width < width:
		height = (1/(image.width/width))*image.height
	else:
		height = image.height/(image.width/width)
	pdb.gimp_image_scale(image, width, height)

def scale_image(width, bg_color, ratio):
	image = gimp.image_list()[0]

	offx = 0
	offy = 0

	# ratio = 3/2 # 1.5
	current_ratio = (image.width/image.height)

	if current_ratio > ratio: # исходная ширина больше
		new_width = image.width
		new_height = image.width*(1/ratio)
		offy = (new_height-image.height)/2
	else:
		new_width = image.width*ratio
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

def scale_and_crop_image(width, bg_color, ratio):
	image = gimp.image_list()[0]
	width = float(width)

	pdb.gimp_context_push()
	pdb.gimp_image_undo_group_start(image)

	pdb.gimp_progress_init("Scaling Image...",None)
	pdb.gimp_context_set_interpolation(INTERPOLATION_LANCZOS) # INTERPOLATION-CUBIC
	
	scale_image(width, bg_color, ratio)
	resize_image(width)

	# Разрешаем запись информации для отмены действий
	pdb.gimp_image_undo_group_end(image)
	pdb.gimp_context_pop()


register(
		 "python-fu-resize-scale",
		 "Приводим изображение к нужному размеру и соотношению сторон",
		 "Меняем размер и обрезаем изображение",
		 "Васин Юрий",
		 "Васин Юрий",
		 "2017",
		 "Resize & scale",
		 "*",
		 [
		  (PF_INT, "width", "New width", 695), # (PF_IMAGE, "image", "Исходное изображение", None),
		  (PF_COLOR, "bg_color",  "Цвет фона", (255,255,255)),
		  (PF_FLOAT, "ratio", "Соотношение сторон (3:2)", 1.5),
		  ],
		 [],
		 scale_and_crop_image,
		 menu="<Image>/DoItUp"
)

main()
