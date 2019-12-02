INSTANCE_ID = '6cdaaede-0a6b-46ff-8080-f0d7c0dd2572'
# This INSTANCE_ID relates with the CONFIGURATION of the SENTINEL.HUB account. I guess we just need one for the App, not one per user

# I obtained this examplecode from: https://sentinelhub-py.readthedocs.io/en/latest/examples/ogc_request.html#Example-1:-True-color-(PNG)-on-a-specific-date
""" The idea would be to get the COORDINATES of the user
in LONGITUD AND LATITUDE, create a BBox with this data,
and search for the latest COPERNICUS image without 
CloudCoverage on it (or with the minimum)"""

import datetime
import numpy as np
import matplotlib.pyplot as plt
from sentinelhub import DataSource
from sentinelhub import CustomUrlParam
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm
from shapely.geometry import Polygon
from sentinelhub import FisRequest, BBox, Geometry, CRS, WcsRequest, CustomUrlParam,DataSource, HistogramType
from sentinelhub.time_utils import iso_to_datetime

from sentinelhub import WmsRequest, WcsRequest, MimeType, CRS, BBox
def plot_image(image, factor=1):
    """
    Utility function for plotting RGB images.
    """
    fig = plt.subplots(1, 1, figsize=(15, 7))

    if np.issubdtype(image.dtype, np.floating):
        plt.imshow(np.minimum(image * factor, 1))
    else:
        plt.imshow(image)
spain_bbox = BBox(bbox=[(-3.303790, 40.116775), (-3.703790, 40.416775)], crs=CRS.WGS84)
#layers = ['SWIR','TRUE-COLOR-S2-L2A','TRUE-COLOR-S2-L1C'] #In case we want to use other data from sentinel apart from RGB images
three_band_req = WmsRequest(layer='TRUE-COLOR-S2-L1C', #Select the layer we want (this has been configured in the CONFIGURATION OPTIONS of the app
                                 bbox=spain_bbox, #Define the LON_LAT box to see
                                 time='latest', #Date of the image, in this case, the latest available
                                 width=512,height=856, #Size of the image in pixels
                                 maxcc=0.01, #Maximim % of cloud coverage. The higher, the more clouds we allow on the image
                                 instance_id=INSTANCE_ID) #The user ID
three_band_img = three_band_req.get_data()
plot_image(three_band_img[-1])
print('These %d images were taken on the following dates:' % len(three_band_img))
for index, date in enumerate(three_band_req.get_dates()):
    print(' - image %d was taken on %s' % (index, date))
plt.show()
