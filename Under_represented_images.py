Python 3.7.4 (v3.7.4:e09359112e, Jul  8 2019, 14:54:52) 
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
>>> def under_represented_images(root_dir):
    full_path = [x for x in os.walk(root_dir)]

    imgs_temp = [os.path.join(ds, f) for ds, _, fs in full_path for f in fs if f]

    length_l_poly = [x for x in imgs_temp if x.__contains__('Lingulodinium_polyedra_guest1')]
    print("The length of l_poly is " + str(len(length_l_poly)))

    length_ciliates = [x for x in imgs_temp if x.__contains__('Ciliate_guest1')]
    print("The length of ciliates is " + str(len(length_ciliates)))

    length_other = [x for x in imgs_temp if x.__contains__('Other_guest1')]
    print("The length of other is " + str(len(length_other)))

    l_poly = [i * 3 for i in imgs_temp if i.__contains__('Lingulodinium_polyedra_guest1')]
    ciliates = [i for i in imgs_temp if i.__contains__('Ciliate_guest1')]
    other = [i for i in imgs_temp if i.__contains__('Other_guest1')]

    all_images = [l_poly + ciliates + other]

    return all_images

under_represented_images(root_dir='/Users/keomonydiep/Documents/Python_practice/Master_images_guest_1_computer')
