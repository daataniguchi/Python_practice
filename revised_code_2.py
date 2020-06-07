Python 3.7.4 (v3.7.4:e09359112e, Jul  8 2019, 14:54:52) 
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
>>> def under_represented_images(root_dir, root_dir_2): ##Specify directory for both guest_1 and guest_3 computers.

    full_path = [x for x in os.walk(root_dir)]
    full_path_2 = [x for x in os.walk(root_dir_2)]

    print(os.walk(root_dir_2))

    imgs_temp = [os.path.join(ds, f) for ds, _, fs in full_path for f in fs if f]
    imgs_temp_2 = [os.path.join(ds, f) for ds, _, fs in full_path_2 for f in fs if f]

    length_l_poly_guest_1 = [x for x in imgs_temp if x.__contains__('Lingulodinium_polyedra_guest1')]
    length_l_poly_guest_3 = [x for x in imgs_temp_2 if x.__contains__('Lingulodinium_polyedra_guest3')]
    print("The length of l_poly is " + str(len(length_l_poly_guest_1 + length_l_poly_guest_3)))


    length_ciliates_guest_1 = [x for x in imgs_temp if x.__contains__('Ciliate_guest1')]
    length_ciliates_guest_3 = [x for x in imgs_temp_2 if x.__contains__('Ciliate_guest3')]
    print("The length of ciliates is " + str(len(length_ciliates_guest_1 + length_ciliates_guest_3)))

    length_other_guest_1 = [x for x in imgs_temp if x.__contains__('Other_guest1')]
    length_other_guest_3 = [x for x in imgs_temp_2 if x.__contains__('Other_guest3')]
    print("The length of other is " + str(len(length_other_guest_1 + length_other_guest_3)))

    length_questionable_guest_1 = [x for x in imgs_temp if x.__contains__('Questionable_guest1')]
    length_questionable_guest_3 = [x for x in imgs_temp_2 if x.__contains__('Questionable_guest3')]
    print("The length of questionable is " + str(len(length_questionable_guest_1 + length_questionable_guest_3)))

    ##categories: Include l_poly, ciliates, other, and questionable

    category_names_guest_1 = [i.rstrip('.DS_Store') for i in os.listdir(root_dir)]

    print(category_names_guest_1)

    category_names_guest_3 = [i.rstrip('.DS_Store') for i in os.listdir(root_dir_2)]

    print(category_names_guest_3)

    l_poly = [length_l_poly_guest_1 + length_l_poly_guest_3]

    ciliates = [length_ciliates_guest_1 + length_ciliates_guest_3]

    other = [length_other_guest_1 + length_other_guest_3]

    questionable = [length_questionable_guest_1 + length_questionable_guest_3]

    all_images = [l_poly + ciliates + other + questionable]

    print(all_images)

    return all_images

under_represented_images(root_dir='/Users/keomonydiep/Documents/Python_practice/Master_images_guest_1_computer', root_dir_2='/Users/keomonydiep/Documents/Python_practice/Master_images_guest_3_computer')
