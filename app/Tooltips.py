# ImageImportPopupDict = {
#     'tresholdBlockSize' : 'Block size for adaptive thresholding (odd number, typically between 3 and 35).',
#     'thresholdC' : 'Constant subtracted from mean in adaptive thresholding (number, typically between 0 and 50).',
#     'applyClahe' : 'Whether to apply CLAHE (contrast enhancement)',
#     'claheClipLimit' : 'Clip limit for CLAHE, higher values enhance contrast more. Positive float, typically between 1.0 and 10.0.',
#     'claheTileGridSize' : 'Tile grid size for CLAHE (usually (8, 8)). Higher resolution images might need larger tile sizes. Each number should be higher than 1. Typical Range: (8, 8) to (32, 32)',
#     'applyMorphology' : 'Whether to apply morphological cleaning (e.g., noise removal).',
#     'applyBlur' : 'Whether to apply Gaussian blur to reduce noise.',
#     'blurKernelSize' : 'Kernel size for the Gaussian blur. Odd integer tuple (3,3) to (7,7); typically (5, 5).',
#     'morphologyKernelSize' : '''The size of the kernel used for the morphological operation (typically 1 or 2). Larger values remove more noise but can also distort shapes.

#     - 1: Minimal cleanup (just removing small noise).

#     - 2 or larger: More aggressive cleaning, good for large noise or artifacts, but may distort thin details.''',
# }
ImageImportToolTipDict = {
    # 'tresholdBlockSize' : (
    #     "The size of the neighborhood (block) used to calculate the adaptive threshold for each pixel.\n"
    #     "\t-35: Larger block size, suitable for larger text regions or more uneven lighting.\n"
    #     "\t15: Smaller block size, better for fine details, but may not handle large varying areas well.\n"
    #     "Range: Odd integers, typically between 3 and 35 (must be odd)"
    # ),

    # "thresholdC" : (
    #     "Constant subtracted from the mean or weighted mean. This helps to adjust the threshold to account for image lighting.\n"
    #     "\t-11: A typical value, works well for average documents with well-defined contrast.\n"
    #     "\t-Higher values: Makes the threshold stricter, useful for bright images.\n"
    #     "\t-Lower values: Makes it more lenient, useful for darker, more contrasty images.\n"
    #     "Range: Integer values in the range of 0 to 50"
    # ),

    "applyClahe": (
        "Whether CLAHE (Contrast Limited Adaptive Histogram Equalization) should be applied to enhance contrast.\n"
        "Set to 'True' to enable CLAHE, 'False' to disable it.\n"
        "When enabled, it improves contrast in images with uneven lighting or backgrounds, helping make details more visible."
    ),
    
    "claheClipLimit": (
        "The contrast enhancement limit for CLAHE.\n"
        "A higher value increases contrast but might introduce artifacts.\n"
        "Recommended values range from 1.0 to 4.0.\n"
        "Typical value: 2.0."
    ),
    
    "claheTileGridSize": (
        "The size of the local tiles for contrast enhancement in CLAHE.\n"
        "Valid values: Odd integers only. Can be square (e.g., (8, 8)) or rectangular (e.g., (10, 20)).\n"
        "Recommended values:\n"
        "- Small (balanced enhancement): (8, 8)\n"
        "- Medium (stronger enhancement): (16, 16)\n"
        "- Large (for large areas with uniform background): (32, 32)\n"
        "- Very large (for very high-res scans): (64, 64)\n"
        "Minimum size: (1, 1)\n"
        "Maximum size: (64, 64)\n"
        "Notes:\n"
        "- Smaller tile sizes work better for detailed areas and irregular textures.\n"
        "- Larger tile sizes work for large, uniform areas but may blur fine details."
    ),

    "applyMorphology":(
        "Whether to apply morphological operations (such as noise removal or shape preservation)."
    ),
    "morphologyKernelSize":(
        "The size of the kernel used for the morphological operation. Larger values remove more noise but can also distort shapes.\n"
        "\t-1: Minimal cleanup (just removing small noise).\n"
        "\t-2 or larger: More aggressive cleaning, good for large noise or artifacts, but may distort thin details.\n"
        "Range: Positive integer (usually 1 or 2)"
    ),
    "blurEnabled": (
        "Whether Gaussian blur should be applied before binarization.\n"
        "Set to 'True' to enable blurring, 'False' to disable it.\n"
        "Blurring is typically used to reduce noise and smooth the image before thresholding."
    ),
    
    "blurKernelSize": (
        "The size of the Gaussian blur kernel.\n"
        "Valid values: Odd integers only (both width and height). Can be square (e.g., (3, 3)) or rectangular (e.g., (5, 3)).\n"
        "Recommended values:\n"
        "- Small (mild blur): (3, 3) or (5, 5)\n"
        "- Medium (balanced blur): (7, 7) or (9, 9)\n"
        "- Large (strong blur): (15, 15) or (21, 21)\n"
        "- Very large (aggressive blur): (31, 31)\n"
        "Minimum size: (3, 3)\n"
        "Maximum size: (31, 31)\n"
        "Notes:\n"
        "- Larger kernels remove more noise but may blur fine details.\n"
        "- Smaller kernels preserve detail but don’t remove much noise.\n"
        "- Kernel dimensions can differ (e.g., (5, 3) for horizontal blur)."
    ),
    
    "invertImage": (
        "Whether the image should be inverted before processing.\n"
        "Set to 'True' to invert the colors, 'False' to keep the original image.\n"
        "Useful when black text on a white background needs to be converted to white text on a black background."
    ),
    
    "thresholdBlockSize": (
        "The size of the local region (block) used for adaptive thresholding.\n"
        "This value should be an odd integer, and it determines how much of the image is used to compute each pixel's threshold.\n"
        "Recommended values: 11 to 21.\n"
        "Too small a block size may result in too much detail, while too large may overly smooth the image."
    ),
    
    "thresholdC": (
        "The constant subtracted from the mean or weighted mean in adaptive thresholding.\n"
        "Helps fine-tune the thresholding by adjusting the local threshold value.\n"
        "Typical values range from 2 to 10.\n"
        "Larger values make the threshold more lenient, smaller values make it more strict."
    )
}
