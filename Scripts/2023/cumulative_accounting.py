from utils import *
# get modules
import arcpy
from pathlib import Path
from great_tables import *
# current working directory
out_chart = local_path.parents[1] / '2023/Cumulative_Accounting'
local_path = pathlib.Path().absolute()
# workspace gdb for stuff that doesnt work in memory
gdb = os.path.join(local_path,'Workspace.gdb')

# get locations
sdeBase = r'F:\GIS\PROJECTS\ResearchAnalysis\ThresholdEvaluation\Vector.sde'
# config, template, and font for the charts
config = {"displayModeBar": False}
template = 'plotly_white'
font     = 'Calibri'

def summarize_landcap_by_parcel(year):
    query = f'"YEAR" = {year}'
    # get paths
    parcelPath  = Path(sdeBase) / 'SDE.Parcels/SDE.Parcel_History_Attributed'
    landcapPath = Path(sdeBase) / 'SDE.Soils/SDE.land_capability_NRCS2007'
    # get parcels where the year is 2023
    parcels = arcpy.management.MakeFeatureLayer(str(parcelPath), 'parcels', query) 
    landcap = arcpy.management.MakeFeatureLayer(str(landcapPath), 'landcap')
    # summarize within
    arcpy.analysis.SummarizeWithin(
        in_polygons=parcels,
        in_sum_features=landcap,
        out_feature_class=fr'C:\\GIS\\Scratch.gdb\\Summarize_ParcelLandCapabalities_{year}',
        keep_all_polygons="KEEP_ALL",
        sum_fields=None,
        sum_shape="ADD_SHAPE_SUM",
        shape_unit="ACRES",
        group_field="Land_Capab",
        add_min_maj="ADD_MIN_MAJ",
        add_group_percent="ADD_PERCENT",
        out_group_table=r"C:\GIS\Scratch.gdb\Land_Capab_Summary"
    )
    arcpy.management.Delete('parcels')
    arcpy.Delete_management("memory")

def summarize_landcap_by_parcel_bailey(year):
    query = f'"YEAR" = {year}'
    # get paths
    parcelPath  = Path(sdeBase) / 'SDE.Parcels/SDE.Parcel_History_Attributed'
    landcapPath = Path(sdeBase) / 'SDE.Soils/SDE.land_capability_Bailey_Soils'
    # get parcels where the year is 2023
    parcels = arcpy.management.MakeFeatureLayer(str(parcelPath), 'parcels', query) 
    landcap = arcpy.management.MakeFeatureLayer(str(landcapPath), 'landcap')
    # summarize within
    arcpy.analysis.SummarizeWithin(
        in_polygons=parcels,
        in_sum_features=landcap,
        out_feature_class=fr'C:\\GIS\\Scratch.gdb\\Summarize_ParcelLandCapabalities_Bailey_{year}',
        keep_all_polygons="KEEP_ALL",
        sum_fields=None,
        sum_shape="ADD_SHAPE_SUM",
        shape_unit="ACRES",
        group_field="CAPABILITY",
        add_min_maj="ADD_MIN_MAJ",
        add_group_percent="ADD_PERCENT",
        out_group_table=r"C:\GIS\Scratch.gdb\Land_Capab_Summary1"
    )
    arcpy.management.Delete('parcels')
    arcpy.Delete_management("memory")

def get_summary(year):
    # get land cap summary as dataframe
    # parcel development layer polygons
    path = fr'C:\GIS\Scratch.gdb\Summarize_ParcelLandCapabalities_Bailey_{year}'
    # query 2022 rows
    sdf = pd.DataFrame.spatial.from_featureclass(path)
    sdf.spatial.sr = sr
    # create new field for Land Capability Category as empty string
    sdf['Category'] = ''
    # set values to 'SEZ' if Majority_Land_Capab = '1B'
    sdf.loc[sdf['Majority_CAPABILITY'].isin(['1B','WB']), 'Category'] = 'SEZ'
    # set values to 'Sensitive' if Majority_Land_Capab = '1C', 1A, 2, 3
    sdf.loc[sdf['Majority_CAPABILITY'].isin(['1C', '1A', '2', '3']), 'Category'] = 'Sensitive'
    # set values to 'Non-Sensitive' if Majority_Land_Capab = '4', 5' or '6' 7
    sdf.loc[sdf['Majority_CAPABILITY'].isin(['4', '5', '6', '7']), 'Category'] = 'Non-Sensitive'
    # filter out WITHIN_TRPA_BOUNDARY = 0
    sdf = sdf.loc[sdf['WITHIN_TRPA_BNDY'] == 1]
    # melt by category and sum Residential_Units, TouristAccommodation_Units, and CommercialFloorArea_SqFt
    df = pd.melt(sdf, id_vars=['Category'], value_vars=['Residential_Units', 'TouristAccommodation_Units', 'CommercialFloorArea_SqFt'], var_name='DevelopmentType', value_name='Value')
    df = df.groupby(['Category', 'DevelopmentType'], dropna=False).sum().reset_index()
    return df, sdf

# get the data
def get_old_dev_cap():
    engine = get_conn('sde_tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM SDE.ThresholdEvaluation_ExistingDevelopmentRights_By_LandCapability", conn)
    return df



def development_by_district():
    import arcpy
    import pandas as pd
    from pathlib import Path

    # Define paths and spatial reference
    sr = arcpy.SpatialReference(4326)  # Example: Use the appropriate spatial reference

    # Set workspace and input feature classes
    arcpy.env.workspace = r""  # Set to your workspace
    parcel_db = Path(sdeBase) / "SDE.Parcel\\SDE.Parcel_History_Attributed"
    sde_districts = Path(sdeBase) / "SDE.Zoning\\SDE.Districts"

    # Load parcel data
    sdf_units = pd.DataFrame.spatial.from_featureclass(parcel_db)
    sdf_units.spatial.sr = sr

    # Load district data
    sdf_districts = pd.DataFrame.spatial.from_featureclass(sde_districts)
    sdf_districts.spatial.sr = sr

    # Define years to process
    years = ['2018', '2019', '2020', '2021', '2022', '2023']

    # Output feature class for the final results
    output_fc = "Development_By_District"

    # Create output feature class if not exists
    if not arcpy.Exists(output_fc):
        arcpy.CreateFeatureclass_management(arcpy.env.workspace, output_fc, "POLYGON", sde_districts)

    # Add necessary fields if they do not exist
    fields_to_add = ['Total_Residential_Units', 'Total_CommercialFloorArea_SqFt', 'Total_TouristAccomodation_Units']
    for field in fields_to_add:
        if field not in [f.name for f in arcpy.ListFields(output_fc)]:
            arcpy.AddField_management(output_fc, field, "DOUBLE")

    # Loop through the years and process data
    for year in years:
        # Filter parcels for the current year
        sdf_units_year = sdf_units[sdf_units['YEAR'] == int(year)]

        # Save filtered dataframe to a temporary feature class for the current year
        year_parcels_fc = f"memory\\parcels_{year}"
        sdf_units_year.spatial.to_featureclass(year_parcels_fc)

        # Perform Spatial Join (parcels with districts) to summarize data by district
        join_output = f"memory\\join_{year}"

        # Create FieldMappings object to define aggregation rules
        field_mappings = arcpy.FieldMappings()

        # Spatial Join with FieldMappings for SUM
        spatial_join = arcpy.analysis.SpatialJoin(
            target_features=sde_districts, 
            join_features=year_parcels_fc, 
            out_feature_class=join_output,
            join_type="KEEP_COMMON",  # Retains only matching parcels and districts
            match_type="INTERSECT",    # Use INTERSECT to join parcels and districts
            field_mapping=field_mappings
        )

        # Create FieldMaps for the fields you want to sum
        residential_units_fieldmap = arcpy.FieldMap()
        residential_units_fieldmap.addInputField(join_output, "Residential_Units")
        residential_units_fieldmap.mergeRule = "SUM"  # Sum Residential_Units
        field_mappings.addFieldMap(residential_units_fieldmap)

        commercial_floor_area_fieldmap = arcpy.FieldMap()
        commercial_floor_area_fieldmap.addInputField(join_output, "CommercialFloorArea_SqFt")
        commercial_floor_area_fieldmap.mergeRule = "SUM"  # Sum CommercialFloorArea_SqFt
        field_mappings.addFieldMap(commercial_floor_area_fieldmap)

        tourist_accommodation_units_fieldmap = arcpy.FieldMap()
        tourist_accommodation_units_fieldmap.addInputField(join_output, "TouristAccomodation_Units")
        tourist_accommodation_units_fieldmap.mergeRule = "SUM"  # Sum TouristAccomodation_Units
        field_mappings.addFieldMap(tourist_accommodation_units_fieldmap)

        # Perform Spatial Join again, this time with field mappings for aggregation
        spatial_join = arcpy.analysis.SpatialJoin(
            target_features=sde_districts, 
            join_features=year_parcels_fc, 
            out_feature_class=join_output,
            join_type="KEEP_ALL",  # Retains only matching parcels and districts
            match_type="INTERSECT",    # Use INTERSECT to join parcels and districts
            field_mapping=field_mappings
        )

        # Append the result to the output feature class
        arcpy.Append_management(join_output, output_fc, "NO_TEST")

        # Clean up temporary in-memory feature classes
        arcpy.Delete_management("memory")

    print("Process completed successfully!")