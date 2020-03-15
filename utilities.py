#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 23:26:04 2020

@author: chaowu
"""

def config_geo_layout(df_conf, px, median_val, current_time):
    
    data = [ dict(
            type = 'scattergeo',
            #locationmode =  #'USA-states',
            locations="iso_alpha",
            lon = df_conf['Long'],
            lat = df_conf['Lat'],
            text = df_conf['text'],
            mode = 'markers',
            marker = dict(
                size = 8,
                opacity = 0.8,
                reversescale = True,
                autocolorscale = False,
                symbol = 'circle',
                line = dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                ),
                # colorscale = scl,
                color_continuous_scale=px.colors.diverging.BrBG,
                color_continuous_midpoint = median_val,
                cmin = 0,
                color = df_conf['total'],
                cmax = df_conf['total'].max(),
                colorbar=dict(
                    title="Confirmed Total"
                )
            ))]
    
    
    layout = dict(
            title = 'CoronaVirus Confirmed Total of ' + current_time ,
            height = 700,
            colorbar = True,
            geo = dict(
                # scope='usa',
                projection= 'natural earth', #dict( type='albers usa' ),
                showland = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(217, 217, 217)",
                countrycolor = "rgb(217, 217, 217)",
                countrywidth = 0.5,
                subunitwidth = 0.5
            ),
        )
            
    return data, layout


