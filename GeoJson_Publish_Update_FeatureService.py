#!/usr/bin/env python
# coding: utf-8

# ## Welcome to your notebook.
# 

# #### Run this cell to connect to your GIS and get started:

# In[ ]:


from arcgis.gis import 
gis = GIS("https://www.arcgis.com", "bsharma_startups", "*****")


# #### Now you are ready to start!

# In[ ]:


#Creating a GeoJson from a feature collection
#conver feature collection to GeoJson
GeoJson = featureset.to_geojson
#upload a geojson
GeoJson = json.loads(GeoJson)
GeoJson


# In[ ]:


#Create a tempfile to store the GeoJson and add as an item to ArcGIS Online Account
import tempfile
from tempfile import mkstemp
def add_geojson(gis, geojson, **item_options):
    """Uploads geojson and returns the file item

    args:
    gis -- gis object where item is added
    geojson -- geojson object to upload as file
    item_options -- additional item properties, see here:
    https://developers.arcgis.com/python/api-reference/arcgis.gis.toc.html#arcgis.gis.ContentManager.add"""

    # get default args
    title = item_options.pop('title')
    tags = item_options.pop('tags')

    # save geojson to tempfile and add as item
    fd, path = tempfile.mkstemp(suffix='.json')
    print(path)

        # with tempfile.NamedTemporaryFile(mode="w") as fp:
    with open(path,'w') as fp:
        fp.write(json.dumps(geojson))
        item = gis.content.add({
            **item_options,
            'type': 'GeoJson',
            'title': title,
            'tags': tags,
        }, data=path)

    return item

        

#Create a scratch layer and publish to a service from geojson (here I am calling add_geojson function mentioned above to create a geojson file and then create a service using "publish")

import logging
def create_scratch_layer(gis, geojson, **item_options):
    """Publishes parsed dataminr geojson as a service and returns the resulting layer item

    Note, use this to quickly add geojson with system default properties. In production,
    it's easier to set desired properties on a template layer then use create_layer."""

    item = add_geojson(gis, geojson, **item_options)
    try:
        lyr_item = item.publish()
    except Exception as e:
        item.delete()
        logging.error('Error creating a new layer: {0}'.format(str(e)))
        return
    item.delete() # if not deleted next run will eror

    # add a unique index for insert operations
    new_index = {
        "name" : "Unique ID", 
        "fields" : "lyr_uid",
        "isUnique" : True,
        "description" : "Unique alert index" 
    }
    add_dict = {"indexes" : [new_index]}
    lyr = lyr_item.layers[0]
    lyr.manager.add_to_definition(add_dict)

    return lyr_item



# In[ ]:


#Search an existing item in your ArcGIS Online account
def get_existing_item(gis, tags=None):
    t = tags if tags else DEFAULT_TAG
    search_items = gis.content.search('tags:"{0}" AND type:"Feature Service"'.format(t))

    return search_items[0] if len(search_items) > 0 else None

#Append to layer (if you want to update a feature service using a geojson using "append" )
def append_to_layer(gis, layer, geojson, uid_field=None):
    item = add_geojson(gis, geojson, title="Data update",tags="Divirod Layer")
    result = None
    try:
        # if there's a uid_field make sure it's indexed before append
        indexes = layer.properties.indexes
        if uid_field and not any(i['fields'] == uid_field for i in indexes):
            _add_unique_index(layer, uid_field)

        result = layer.append(
            item_id=item.id,
            upload_format="geojson",
            upsert=(uid_field != None),
            upsert_matching_field=uid_field # update existing features with matching uid_fields
        )
    finally:
        item.delete() # if not deleted next run will eror and pollute ArcGIS

   
    return result

#Check if you have the existing layer and can append it or create the layer from scratch 
def add_update_layer(gis, geojson, title, tags):
    item = get_existing_item(gis, tags=tags)
    out = None
    if item:
        lyr = item.layers[0]
        append_to_layer(gis, lyr, geojson,uid_field=None)
        return item
    else:
        return create_scratch_layer(gis, geojson, title=title, tags=tags)
        
#Here, we are calling the add_update_layer function and we are passing the paramters
#In "get_existing_item" fucntion it looks for the divirod layer if it doesn't exist then calls the "create_scratch_layer"  or if layer exists then updates the existing layer using "append_to_layer" function
add_update_layer(gis, GeoJson, title="Divirod_Layer",tags="Divirod Layer")

print("item created")

