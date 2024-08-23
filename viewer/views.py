import folium
from django.shortcuts import render
from .utils import get_raster_data
import os
from django.conf import settings
from pyproj import Transformer

def map_view(request):
    try:
        raster_info = get_raster_data('/app/data/export_result.tif')
        print("Raster info loaded successfully")
    except Exception as e:
        print(f"Error loading raster: {e}")
        return render(request, 'viewer/error.html', {'error_message': str(e)})

    try:
        # Convertir les coordonnées
        transformer = Transformer.from_crs("EPSG:32633", "EPSG:4326", always_xy=True)
        bottom_left = transformer.transform(raster_info["bounds"].left, raster_info["bounds"].bottom)
        top_right = transformer.transform(raster_info["bounds"].right, raster_info["bounds"].top)

        # Calculer le centre de la carte
        center_lat = (bottom_left[1] + top_right[1]) / 2
        center_lon = (bottom_left[0] + top_right[0]) / 2

        # Créer la carte centrée sur le fichier Raster
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
        print("Map created successfully")

        # Ajouter la bordure rouge
        bounds_polygon = [
            [bottom_left[1], bottom_left[0]],
            [bottom_left[1], top_right[0]],
            [top_right[1], top_right[0]],
            [top_right[1], bottom_left[0]],
            [bottom_left[1], bottom_left[0]]
        ]
        folium.Polygon(
            locations=bounds_polygon,
            color='red',
            fill=False,
            weight=2
        ).add_to(m)
        
        image_overlay = folium.raster_layers.ImageOverlay(
            image='/app/data/export_result.tif',
            bounds=[bottom_left, top_right],
            opacity=0.7,
            interactive=True,
            cross_origin=False,
            zindex=1
        )
        
        image_overlay.add_to(m)
        print("Image overlay added successfully")
        
        return render(request, 'viewer/map.html', {'map': m._repr_html_()})
    except Exception as e:
        print(f"Error rendering map: {e}")
        return render(request, 'viewer/error.html', {'error_message': str(e)})

