# Condition that removes all the rectangles and parallelograms except the first parallelogram

import streamlit as st
import zipfile
import io
import json

st.title('PowerBI Accelerator by Sigmoid')

# Upload the Source zip file
ss = st.file_uploader('Upload a PBIX file')

# --------- Removing Streamlit's Hamburger and Footer starts ---------
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            a {text-decoration: none;}
            .css-15tx938 {font-size: 18px !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# --------- Removing Streamlit's Hamburger and Footer ends ------------
new_vc1 = {
    "id": 99999999,
    "x": 0,
    "y": 0,
    "z": 15000,
    "width": 1440.3516483516485,
    "height": 65,
    "config": "{\"name\":\"be03e83f8af4ed66720d\",\"layouts\":[{\"id\":0,\"position\":{\"x\":0,\"y\":0,\"z\":15000,\"width\":1440.3516483516485,\"height\":65,\"tabOrder\":15000}}],\"singleVisual\":{\"visualType\":\"shape\",\"drillFilterOtherVisuals\":true,\"objects\":{\"shape\":[{\"properties\":{\"tileShape\":{\"expr\":{\"Literal\":{\"Value\":\"'rectangle'\"}}},\"tabRoundCornerTop\":{\"expr\":{\"Literal\":{\"Value\":\"20L\"}}}}}],\"rotation\":[{\"properties\":{\"shapeAngle\":{\"expr\":{\"Literal\":{\"Value\":\"0L\"}}}}}],\"fill\":[{\"properties\":{\"fillColor\":{\"solid\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#00519C'\"}}}}}},\"selector\":{\"id\":\"default\"}}]},\"vcObjects\":{\"title\":[{\"properties\":{\"text\":{\"expr\":{\"Literal\":{\"Value\":\"'Report title background'\"}}}}}]}}}",
    "filters": "[]",
    "tabOrder": 15000
}

new_vc2 = {
                    "id": 2539326977,
                    "x": 355,
                    "y": 11,
                    "z": 38000,
                    "width": 768,
                    "height": 64.71910112359551,
                    "config": "{\"name\":\"1ee7ff6475ab1fbc89b7\",\"layouts\":[{\"id\":0,\"position\":{\"x\":355,\"y\":11,\"z\":38000,\"width\":768,\"height\":64.71910112359551,\"tabOrder\":38000}}],\"singleVisual\":{\"visualType\":\"textbox\",\"drillFilterOtherVisuals\":true,\"objects\":{\"general\":[{\"properties\":{\"paragraphs\":[{\"textRuns\":[{\"value\":\"TIC Code Consumer All Brands Gross Inv Report\",\"textStyle\":{\"fontWeight\":\"bold\",\"fontSize\":\"20pt\",\"color\":\"#ffffff\"}}]}]}}]},\"vcObjects\":{\"background\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}]}}}",
                    "filters": "[]",
                    "tabOrder": 38000
                }

footer_text={
    "x": 39.52191235059761,
    "y": 657.8486055776892,
    "z": 5000,
    "width": 140.23904382470118,
    "height": 36.972111553784856,
    "config": "{\"name\":\"a145d8869e65ef7d44fd\",\"layouts\":[{\"id\":0,\"position\":{\"x\":39.52191235059761,\"y\":657.8486055776892,\"z\":5000,\"width\":140.23904382470118,\"height\":36.972111553784856,\"tabOrder\":5000}}],\"singleVisual\":{\"visualType\":\"textbox\",\"drillFilterOtherVisuals\":true,\"objects\":{\"general\":[{\"properties\":{\"paragraphs\":[{\"textRuns\":[{\"value\":\"Source: \",\"textStyle\":{\"fontWeight\":\"bold\",\"fontSize\":\"14pt\"}}]}]}}]}}}",
    "filters": "[]",
    "tabOrder": 5000
}

ibutton={
                    "x": 1216.2549800796812,
                    "y": 11.47410358565737,
                    "z": 1100000,
                    "width": 43.34661354581673,
                    "height": 39.52191235059761,
                    "config": "{\"name\":\"88af22203e111f0690dd\",\"layouts\":[{\"id\":0,\"position\":{\"x\":1216.2549800796812,\"y\":11.47410358565737,\"z\":1100000,\"width\":43.34661354581673,\"height\":39.52191235059761,\"tabOrder\":1100000}}],\"singleVisual\":{\"visualType\":\"actionButton\",\"drillFilterOtherVisuals\":true,\"objects\":{\"icon\":[{\"properties\":{\"shapeType\":{\"expr\":{\"Literal\":{\"Value\":\"'information'\"}}},\"lineColor\":{\"solid\":{\"color\":{\"expr\":{\"ThemeDataColor\":{\"ColorId\":0,\"Percent\":0}}}}}},\"selector\":{\"id\":\"default\"}}]},\"vcObjects\":{\"visualLink\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"type\":{\"expr\":{\"Literal\":{\"Value\":\"'WebUrl'\"}}},\"webUrl\":{\"expr\":{\"Literal\":{\"Value\":\"'https://www.sigmoid.com/'\"}}}}}],\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}]}},\"howCreated\":\"InsertVisualButton\"}",
                    "filters": "[]",
                    "tabOrder": 1100000
                }

footer_box={
    "x": 19.123505976095615,
    "y": 643.8247011952191,
    "z": 4000,
    "width": 1240.4780876494024,
    "height": 62.470119521912345,
    "config": "{\"name\":\"fa8e2fe72928be0b6366\",\"layouts\":[{\"id\":0,\"position\":{\"x\":19.123505976095615,\"y\":643.8247011952191,\"z\":4000,\"width\":1240.4780876494024,\"height\":62.470119521912345,\"tabOrder\":4000}}],\"singleVisual\":{\"visualType\":\"shape\",\"drillFilterOtherVisuals\":true,\"objects\":{\"shape\":[{\"properties\":{\"tileShape\":{\"expr\":{\"Literal\":{\"Value\":\"'rectangle'\"}}}}}],\"rotation\":[{\"properties\":{\"shapeAngle\":{\"expr\":{\"Literal\":{\"Value\":\"0L\"}}}}}],\"outline\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}],\"fill\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}}}},{\"properties\":{\"fillColor\":{\"solid\":{\"color\":{\"expr\":{\"ThemeDataColor\":{\"ColorId\":0,\"Percent\":0}}}}}},\"selector\":{\"id\":\"default\"}}]},\"vcObjects\":{\"background\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"transparency\":{\"expr\":{\"Literal\":{\"Value\":\"0D\"}}}}}],\"title\":[{\"properties\":{\"titleWrap\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"fontColor\":{\"solid\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#00519C'\"}}}}},\"background\":{\"solid\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#FFFFFF'\"}}}}},\"alignment\":{\"expr\":{\"Literal\":{\"Value\":\"'left'\"}}},\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"'16'\"}}},\"bold\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"fontFamily\":{\"expr\":{\"Literal\":{\"Value\":\"'Segoe UI'\"}}}}}],\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"color\":{\"solid\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#CCCCCC'\"}}}}},\"radius\":{\"expr\":{\"Literal\":{\"Value\":\"7D\"}}}}}],\"dropShadow\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"preset\":{\"expr\":{\"Literal\":{\"Value\":\"'Center'\"}}},\"position\":{\"expr\":{\"Literal\":{\"Value\":\"'Outer'\"}}},\"color\":{\"solid\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#808080'\"}}}}}}}]}},\"howCreated\":\"InsertVisualButton\"}",
    "filters": "[]",
    "tabOrder": 4000
}

source_text={
                    "x": 122.39043824701194,
                    "y": 656.5737051792828,
                    "z": 12001,
                    "width": 140.23904382470118,
                    "height": 36.972111553784856,
                    "config": "{\"name\":\"a7ec1ed60550297610b7\",\"layouts\":[{\"id\":0,\"position\":{\"x\":122.39043824701194,\"y\":656.5737051792828,\"z\":12001,\"width\":140.23904382470118,\"height\":36.972111553784856,\"tabOrder\":12001}}],\"singleVisual\":{\"visualType\":\"textbox\",\"drillFilterOtherVisuals\":true,\"objects\":{\"general\":[{\"properties\":{\"paragraphs\":[{\"textRuns\":[{\"value\":\"Inventory Data \",\"textStyle\":{\"fontSize\":\"14pt\"}}]}]}}]}}}",
                    "filters": "[]",
                    "tabOrder": 12001
                }

bar={
                    "x": 19,
                    "y": 255,
                    "z": 0,
                    "width": 407,
                    "height": 362,
                    "config": "{\"name\": \"ec2b436d7f5655cb2ed8\", \"layouts\": [{\"id\": 0, \"position\": {\"x\": 19, \"y\": 255, \"z\": 0, \"width\": 407, \"height\": 362, \"tabOrder\": 0}}], \"singleVisual\": {\"visualType\": \"barChart\", \"projections\": {\"Category\": [{\"queryRef\": \"Orders.Category\", \"active\": true}], \"Y\": [{\"queryRef\": \"Sum(Orders.Sales)\"}]}, \"prototypeQuery\": {\"Version\": 2, \"From\": [{\"Name\": \"o\", \"Entity\": \"Orders\", \"Type\": 0}], \"Select\": [{\"Column\": {\"Expression\": {\"SourceRef\": {\"Source\": \"o\"}}, \"Property\": \"Category\"}, \"Name\": \"Orders.Category\", \"NativeReferenceName\": \"Category\"}, {\"Aggregation\": {\"Expression\": {\"Column\": {\"Expression\": {\"SourceRef\": {\"Source\": \"o\"}}, \"Property\": \"Sales\"}}, \"Function\": 0}, \"Name\": \"Sum(Orders.Sales)\", \"NativeReferenceName\": \"Sales\"}], \"OrderBy\": [{\"Direction\": 2, \"Expression\": {\"Aggregation\": {\"Expression\": {\"Column\": {\"Expression\": {\"SourceRef\": {\"Source\": \"o\"}}, \"Property\": \"Sales\"}}, \"Function\": 0}}}]}, \"columnProperties\": {\"Sum(Orders.Sales)\": {\"displayName\": \"Sales\"}}, \"drillFilterOtherVisuals\": true, \"hasDefaultSort\": true, \"vcObjects\": {\"border\": [{\"properties\": {\"color\": {\"solid\": {\"color\": {\"expr\": {\"Literal\": {\"Value\": \"'#CCCCCC'\"}}}}}}}], \"title\": [{\"properties\": {\"fontFamily\": {\"expr\": {\"Literal\": {\"Value\": \"'Segoe UI'\"}}}, \"fontSize\": {\"expr\": {\"Literal\": {\"Value\": 16}}}}}]}}}",
                    "filters": "[]",
                    "query": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"o\",\"Entity\":\"Orders\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"o\"}},\"Property\":\"Category\"},\"Name\":\"Orders.Category\",\"NativeReferenceName\":\"Category\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"o\"}},\"Property\":\"Sales\"}},\"Function\":0},\"Name\":\"Sum(Orders.Sales)\",\"NativeReferenceName\":\"Sales\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"o\"}},\"Property\":\"Sales\"}},\"Function\":0}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":1000}}},\"Version\":1},\"ExecutionMetricsKind\":1}}]}",
                    "dataTransforms": "{\"projectionOrdering\":{\"Category\":[0],\"Y\":[1]},\"projectionActiveItems\":{\"Category\":[{\"queryRef\":\"Orders.Category\",\"suppressConcat\":false}]},\"queryMetadata\":{\"Select\":[{\"Restatement\":\"Category\",\"Name\":\"Orders.Category\",\"Type\":2048},{\"Restatement\":\"Sales\",\"Name\":\"Sum(Orders.Sales)\",\"Type\":1}]},\"visualElements\":[{\"DataRoles\":[{\"Name\":\"Category\",\"Projection\":0,\"isActive\":true},{\"Name\":\"Y\",\"Projection\":1,\"isActive\":false}]}],\"selects\":[{\"displayName\":\"Category\",\"queryName\":\"Orders.Category\",\"roles\":{\"Category\":true},\"type\":{\"category\":null,\"underlyingType\":1},\"expr\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Entity\":\"Orders\"}},\"Property\":\"Category\"}}},{\"displayName\":\"Sales\",\"queryName\":\"Sum(Orders.Sales)\",\"roles\":{\"Y\":true},\"sort\":2,\"sortOrder\":0,\"type\":{\"category\":null,\"underlyingType\":259},\"expr\":{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Entity\":\"Orders\"}},\"Property\":\"Sales\"}},\"Function\":0}}}]}"
                }

simage=                            {
                    "x": 30,
                    "y": 5,
                    "z": 11111000,
                    "width": 183.375,
                    "height": 51.75,
                    "config": "{\"name\":\"08011354e84b647e1de6\",\"layouts\":[{\"id\":0,\"position\":{\"x\":30,\"y\":5,\"z\":11111000,\"width\":183.375,\"height\":51.75,\"tabOrder\":11000}}],\"singleVisual\":{\"visualType\":\"image\",\"drillFilterOtherVisuals\":true,\"objects\":{\"general\":[{\"properties\":{\"imageUrl\":{\"expr\":{\"ResourcePackageItem\":{\"PackageName\":\"RegisteredResources\",\"PackageType\":1,\"ItemName\":\"image_(10)09472004764938458.png\"}}}}}]}}}",
                    "filters": "[]",
                    "tabOrder": 11000
                }

if ss:
    #st.info('Select one of the option')
    #radio=st.radio(' ', ['Add new Header','Update exisiting Header'])

    if 1==1:
        # In-memory byte stream to hold the destination zip file data
        zip_data = io.BytesIO()

        # Extract the files from the source zip file and re-zip them into a destination zip file
        with zipfile.ZipFile(ss, 'r') as source_zip:
            with zipfile.ZipFile(zip_data, 'w') as destination_zip:
                # Iterate over the files in the source zip file
                for name in source_zip.namelist():

                    # Skip the Security Binding file
                    if name == 'SecurityBindings':
                        continue

                    # Manipulate the Layout file
                    if name == 'Report/Layout':
                        # Read the contents of the layout file
                        data = source_zip.read(name).decode('utf-16 le')
                        # Old layout file
                        with open('app-og.json', 'w') as f:
                            a=json.loads(data)
                            json.dump(a, f)
                        try:
                            data=json.loads(data)
                            ##### Changing attributes of certain elements
                            for section in data['sections']:
                                # print(section,'section')
                                section['visualContainers'].append(new_vc1)
                                section['visualContainers'].append(new_vc2)
                                section['visualContainers'].append(footer_text)
                                section['visualContainers'].append(footer_box)
                                section['visualContainers'].append(ibutton)
                                section['visualContainers'].append(source_text)
                                section['visualContainers'].append(simage)
                                if section['ordinal'] == 0:  # Checking if it's the first page
                                    for visual in section['visualContainers']:
                                         # Load the config dictionary from the JSON string
                                        config = json.loads(visual['config'])

                                        try:
                                            config['singleVisual']['vcObjects']['title'][0]['properties']['fontFamily']['expr']['Literal']['Value']="'Segoe UI'"
                                            config['singleVisual']['vcObjects']['title'][0]['properties']['fontSize']['expr']['Literal']['Value']=16
                                            visual['config']=json.dumps(config)
                                            #st.write(visual['config'])
                                        except:
                                                print('tested')

                                        # Application 2 - Changing position of line chart
                                        if config['singleVisual']['visualType'] == 'lineChart':
                                            #st.write('found line chart in page 1')
                                        
                                            # Update main dictionary values
                                            visual['x'] = 886
                                            visual['y'] = 255
                                            visual['width'] = 373
                                            visual['height'] = 363
                                            for layout in config['layouts']:
                                                # Update the values in the config dictionary
                                                #st.write('inside config dict')
                                                layout['position']['x'] = 886
                                                layout['position']['y'] = 255
                                                layout['position']['width'] = 373
                                                layout['position']['height'] = 363
                                                #st.write(layout['position']['x'],layout['position']['y'])
                                        visual['config']=json.dumps(config)
                                        #st.write(visual['config'])
                                        
                                        # Pie chart
                                        if config['singleVisual']['visualType'] == 'tableEx':
                                            #st.write('found pie chart in page 1')
                                        
                                            # Update main dictionary values
                                            visual['x'] = 20
                                            visual['y'] = 186
                                            visual['width'] = 1239
                                            visual['height'] = 453
                                            for layout in config['layouts']:
                                                # Update the values in the config dictionary
                                                #st.write('inside config dict')
                                                layout['position']['x'] = 20
                                                layout['position']['y'] = 186
                                                layout['position']['width'] = 1239
                                                layout['position']['height'] = 453
                                                #st.write(layout['position']['x'],layout['position']['y'])
                                        visual['config']=json.dumps(config)
                                        #st.write(visual['config'])

                                        # Bar chart
                                        if config['singleVisual']['visualType'] == 'barChart':
                                            #st.write('found bar chart in page 1')
                                        
                                            # Update main dictionary values
                                            visual['x'] = 19
                                            visual['y'] = 255
                                            visual['width'] = 407
                                            visual['height'] = 362
                                            for layout in config['layouts']:
                                                # Update the values in the config dictionary
                                                #st.write('inside config dict')
                                                layout['position']['x'] = 19
                                                layout['position']['y'] = 255
                                                layout['position']['width'] = 407
                                                layout['position']['height'] = 362
                                                #st.write(layout['position']['x'],layout['position']['y'])
                                        visual['config']=json.dumps(config)
                                        #st.write(visual['config'])

                                        # try:
                                        #     st.write(config['singleVisual']['vcObjects']['title'][0]['properties']['fontFamily']['expr']['Literal']['Value'])
                                        # except:
                                        #     st.write('huh')
                                        # if 'fontFamily' in config['singleVisual']['objects']['general'][0]['properties']:
                                        #     st.write('hi')
                                        #     visual['config']=json.dumps(config)
                                        #     st.write('Diff font found')
                                        #     st.write(config['singleVisual']['objects']['general'][0]['properties']['fontFamily']['expr']['Literal']['Value'])
                                        #     # Update the config in the visual container
                                        #     visual['config'] = json.dumps(config)
                                        #     st.write(visual['config'])

                                else:
                                    for visual in section['visualContainers']:
                                        config = json.loads(visual['config'])
                                        try:
                                            #st.write('inside second page')
                                            config['singleVisual']['vcObjects']['title'][0]['properties']['fontFamily']['expr']['Literal']['Value']="'Segoe UI'"
                                            config['singleVisual']['vcObjects']['title'][0]['properties']['fontSize']['expr']['Literal']['Value']=16
                                            visual['config']=json.dumps(config)
                                            #st.write(visual['config'])
                                        except:
                                            print('tested')
                            # New Layout file
                            with open('app-generated.json', 'w') as f:
                                json.dump(data, f)
                        
                        except:
                            print('hi')
                        # Add the manipulated layout data to the destination zip file
                        data = json.dumps(data)
                        destination_zip.writestr(name, data.encode('utf-16 le'))
                    
                    else:
                        # Add the file to the destination zip file as-is
                        binary_data = source_zip.read(name)
                        destination_zip.writestr(name, binary_data)


        # Download the destination file
        st.download_button(
            label='Download Destination PBIX File',
            data=zip_data.getvalue(),
            file_name='destination.pbix',
            mime='application/pbix'
        )
    elif 1==2:
        # In-memory byte stream to hold the destination zip file data
        zip_data = io.BytesIO()

        # Extract the files from the source zip file and re-zip them into a destination zip file
        with zipfile.ZipFile(ss, 'r') as source_zip:
            with zipfile.ZipFile(zip_data, 'w') as destination_zip:
                # Iterate over the files in the source zip file
                for name in source_zip.namelist():

                    # Skip the Security Binding file
                    if name == 'SecurityBindings':
                        continue

                    # Manipulate the Layout file
                    if name == 'Report/Layout':
                        # Read the contents of the layout file
                        data = source_zip.read(name).decode('utf-16 le')

                        # Old layout file
                        with open('og_file.json', 'w') as f:
                            a=json.loads(data)
                            json.dump(a, f)
                        try:
                            ##### Removing certain elements
                            data=json.loads(data)
                            for section in data['sections']:
                                print(section)

                                # Create a new list of visual containers that don't meet the condition
                                new_visual_containers = []
                                for visualContainer in section['visualContainers']:
                                    # Check if y is 0 and x is >500 and config contains "parallelogram" or "rectangle"
                                    if visualContainer['y'] == 0 and visualContainer['x'] > 500 and ("parallelogram" in visualContainer['config'] or "rectangle" in visualContainer['config']):
                                        continue
                                    else:
                                        new_visual_containers.append(visualContainer)

                                # Replace the old list with the new list
                                section['visualContainers'] = new_visual_containers
                            
                            ##### Changing attributes of certain elements
                            for section in data['sections']:
                                for visualContainer in section['visualContainers']:

                                    # Changing Header rectangle
                                    if visualContainer['y'] == 0 and "#004E90" in visualContainer['config'] :
                                        # Change x, height, and width
                                        visualContainer['x'] = 0
                                        visualContainer['height'] = 65
                                        visualContainer['width'] = 1280
                                        # Change config
                                        config = json.loads(visualContainer['config'])

                                        # Parallelogram to Rectangle
                                        # Replace "parallelogram" with "rectangle" in the "config" key's value
                                        config["singleVisual"]["objects"]["shape"][0]["properties"]["tileShape"]["expr"]["Literal"]["Value"] = "'rectangle'"

                                        for layout in config['layouts']:
                                            layout['position']['x'] = 0
                                            layout['position']['height'] = 65
                                            layout['position']['width'] = 1280 
                                        visualContainer['config'] = json.dumps(config)

                                    # Changing z of logo
                                    if visualContainer['y'] == 0 and "Pepsico_4659666136978873.png" in visualContainer['config']:
                                        visualContainer['z'] = 50000
                                        # Change config
                                        config = json.loads(visualContainer['config'])
                                        for layout in config['layouts']:
                                            layout['position']['z'] = 50000
                                        visualContainer['config'] = json.dumps(config)

                                    # Changing attributes of groups
                                    if visualContainer['y'] == 0 and "singleVisualGroup" in visualContainer['config']:
                                        visualContainer['x'] = 0
                                        visualContainer['height'] = 65
                                        visualContainer['width'] = 1280
                                        # Change config
                                        config = json.loads(visualContainer['config'])
                                        for layout in config['layouts']:
                                            layout['position']['x'] = 0
                                            layout['position']['height'] = 65
                                            layout['position']['width'] = 1280
                                        visualContainer['config'] = json.dumps(config)
                            
                            # New Layout file
                            with open('updated_file.json', 'w') as f:
                                json.dump(data, f)
                        
                        except:
                            print('hi')
                        # Add the manipulated layout data to the destination zip file
                        data = json.dumps(data)
                        destination_zip.writestr(name, data.encode('utf-16 le'))
                    
                    else:
                        # Add the file to the destination zip file as-is
                        binary_data = source_zip.read(name)
                        destination_zip.writestr(name, binary_data)


        # Download the destination file
        st.download_button(
            label='Download Destination PBIX File',
            data=zip_data.getvalue(),
            file_name='destination.pbix',
            mime='application/pbix'
        )
    else:
        print('')
