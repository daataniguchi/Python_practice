Python 3.7.4 (v3.7.4:e09359112e, Jul  8 2019, 14:54:52) 
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
>>> def func_2():
    root_dir = '/Users/keomonydiep/Desktop/training_images'

    full_path = [x for x in os.walk(root_dir)]

    imgs_temp = [os.path.join(ds, f) for ds, _, fs in full_path for f in fs if f]

    under_represented_l_poly = [i * 2 for i in imgs_temp if i.__contains__('l_poly')]
    under_represented_ciliates = [i * 4 for i in imgs_temp if i.__contains__('ciliates')]
    over_represented_other = [i for i in imgs_temp if i.__contains__('other')]

    all_images = [under_represented_ciliates + under_represented_l_poly + over_represented_other]

    print(all_images)

func_2()
