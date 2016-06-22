#!flask/bin/python

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps                     
from flask import render_template

app = Flask(__name__)
api = Api(app)
                                          
# Testing stuff

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('index.html')                              
     

                   
# used for the form post handling
@app.route('/parcel/', methods=['GET', 'POST'])
def parcel():
    parcel_id=request.form['parcel_id'] 
    return render_template('parcel_map.html', parcel_id=parcel_id)   
    
# attempt to use for more general info
@app.route('/inspire_parcel/<inspire_id>')
def hello(inspire_id=None):
    return render_template('inspire_parcel_map.html', inspire_id=inspire_id)
	
@app.route('/postcode/', methods=['POST'])
def postcode():
    postcode_id1=request.form['postcode_id1']   
    postcode_id2=request.form['postcode_id2'] 
    return render_template('postcode_map.html', postcode_id1=postcode_id1, postcode_id2=postcode_id2)  



# Class definitions for the endpoints:


# Inspire Polygons 		

class InspireParcel(Resource):
    def get(self, inspire_id):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, a.gml_id, a.valid_from_dt, a.begin_lifespan_dt, a.area_sqkm, a.area_sqmi, a.acres FROM inspire a WHERE a.inspire_id='%s'"%inspire_id)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result            

class InspireParcelPoly(Resource):
    def get(self, inspire_id):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_poly FROM inspire a WHERE a.inspire_id='%s'"%inspire_id)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result  

class InspirePostcode(Resource):
    def get(self, pc1, pc2):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, a.gml_id, a.valid_from_dt, a.begin_lifespan_dt, a.area_sqkm, a.area_sqmi, a.acres, b.overlap_pc FROM inspire a, mapping_lsoa b, lsoa c WHERE a.inspire_id=b.inspire_id AND b.lsoa_11_cd = c.lsoa_11_cd AND c.postcode = '%s %s'" % (pc1, pc2))
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result


# Land Classification

class ALCParcel(Resource):
    def get(self, inspire_id):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.alc_grade, e.alc_spatial_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_alc d, alc e WHERE a.inspire_id = d.inspire_id AND d.ogr_fid = e.ogr_fid AND a.inspire_id='%s'"%inspire_id)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class ALCPostcode(Resource):
    def get(self, pc1, pc2):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.alc_grade, e.alc_spatial_poly FROM inspire a, mapping_lsoa b, lsoa c, mapping_alc d, alc e WHERE a.inspire_id=b.inspire_id AND b.lsoa_11_cd = c.lsoa_11_cd AND a.inspire_id = d.inspire_id AND d.ogr_fid = e.ogr_fid AND c.postcode = '%s %s'" % (pc1, pc2))
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result		
		

# Conservation Areas

class ConservationParcel(Resource):
    def get(self, inspire_id):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.conservation_key, e.wak, e.sssi_name, e.owner_title, e.owner_name, e.owner_org, e.start_date, e.expire_date, e.area, e.theme, e.theme_id, e.amount, e.conservation_area_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_conservation d, conservation e WHERE a.inspire_id = d.inspire_id AND d.conservation_key = e.conservation_key AND a.inspire_id='%s'"%inspire_id)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class ConservationPostcode(Resource):
    def get(self, pc1, pc2):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.conservation_key, e.wak, e.sssi_name, e.owner_title, e.owner_name, e.owner_org, e.start_date, e.expire_date, e.area, e.theme, e.theme_id, e.amount, e.conservation_area_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_lsoa b, lsoa c, mapping_conservation d, conservation e WHERE a.inspire_id=b.inspire_id AND b.lsoa_11_cd = c.lsoa_11_cd AND a.inspire_id = d.inspire_id AND d.conservation_key = e.conservation_key AND c.postcode = '%s %s'" % (pc1, pc2))
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result		
		

# Contours

class ContoursParcel(Resource):
    def get(self, inspire_id):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, e.id, e.feat_type, e.sub_type, e.prop_value, e.contours_line FROM inspire a, mapping_contours d, contours e WHERE a.inspire_id = d.inspire_id AND d.id = e.id AND a.inspire_id='%s'"%inspire_id)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class ContoursPostcode(Resource):
    def get(self, pc1, pc2):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, e.id, e.feat_type, e.sub_type, e.prop_value, e.contours_line FROM inspire a, mapping_lsoa b, lsoa c, mapping_contours d, contours e WHERE a.inspire_id=b.inspire_id AND b.lsoa_11_cd = c.lsoa_11_cd AND a.inspire_id = d.inspire_id AND d.id = e.id AND c.postcode = '%s %s'" % (pc1, pc2))
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

# Flood Alerts

class FloodAlertsParcel(Resource):
    def get(self, inspire_id):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.region, e.area, e.fwd_tacode, e.fwis_code, e.fwa_name, e.descrip, e.river_sea, e.county, e.e_qdial, e.w_region, e.w_fwa_name, e.w_descrip, e.w_afon, e.w_qdial, e.flood_alert_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_flood_alerts d, flood_alerts e WHERE a.inspire_id = d.inspire_id AND d.fwis_code = e.fwis_code AND a.inspire_id='%s'"%inspire_id)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class FloodAlertsPostcode(Resource):
    def get(self, pc1, pc2):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.region, e.area, e.fwd_tacode, e.fwis_code, e.fwa_name, e.descrip, e.river_sea, e.county, e.e_qdial, e.w_region, e.w_fwa_name, e.w_descrip, e.w_afon, e.w_qdial, e.flood_alert_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_lsoa b, lsoa c, mapping_flood_alerts d, flood_alerts e WHERE a.inspire_id=b.inspire_id AND b.lsoa_11_cd = c.lsoa_11_cd AND a.inspire_id = d.inspire_id AND d.fwis_code = e.fwis_code AND c.postcode = '%s %s'" % (pc1, pc2))
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

#Flood Risks

class FloodRisksParcel(Resource):
    def get(self, inspire_id):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.flood_risk_key, e.fra_name, e.country, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_flood_risks d, flood_risks e WHERE a.inspire_id = d.inspire_id AND d.flood_risk_key = e.flood_risk_key AND a.inspire_id='%s'"%inspire_id)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class FloodRisksPostcode(Resource):
    def get(self, pc1, pc2):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.flood_risk_key, e.fra_name, e.country, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_lsoa b, lsoa c, mapping_flood_risks d, flood_risks e WHERE a.inspire_id=b.inspire_id AND b.lsoa_11_cd = c.lsoa_11_cd AND a.inspire_id = d.inspire_id AND d.flood_risk_key = e.flood_risk_key AND c.postcode = '%s %s'" % (pc1, pc2))
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

# Flood Warnings

class FloodWarningsParcel(Resource):
    def get(self, inspire_id):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.region, e.area, e.fwd_tacode, e.fwis_code, e.fwa_name, e.descrip, e.river_sea, e.county, e.e_qdial, e.w_region, e.w_fwa_name, e.w_descrip, e.w_afon, e.w_qdial, e.flood_warning_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_flood_warnings d, flood_warnings e WHERE a.inspire_id = d.inspire_id AND d.fwis_code = e.fwis_code AND a.inspire_id='%s'"%inspire_id)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class FloodWarningsPostcode(Resource):
    def get(self, pc1, pc2):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.region, e.area, e.fwd_tacode, e.fwis_code, e.fwa_name, e.descrip, e.river_sea, e.county, e.e_qdial, e.w_region, e.w_fwa_name, e.w_descrip, e.w_afon, e.w_qdial, e.flood_warning_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_lsoa b, lsoa c, mapping_flood_warnings d, flood_warnings e WHERE a.inspire_id=b.inspire_id AND b.lsoa_11_cd = c.lsoa_11_cd AND a.inspire_id = d.inspire_id AND d.fwis_code = e.fwis_code AND c.postcode = '%s %s'" % (pc1, pc2))
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

# Hydrogeology

class HydrogeologyParcel(Resource):
    def get(self, inspire_id):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.object_id, e.rock_unit, e.class, e.character, e.flow_mech, e.summary, e.version, e.hydrogeology_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_hydrogeology d, hydrogeology e WHERE a.inspire_id = d.inspire_id AND d.object_id = e.object_id AND a.inspire_id='%s'"%inspire_id)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class HydrogeologyPostcode(Resource):
    def get(self, pc1, pc2):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.object_id, e.rock_unit, e.class, e.character, e.flow_mech, e.summary, e.version, e.hydrogeology_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_lsoa b, lsoa c, mapping_hydrogeology d, hydrogeology e WHERE a.inspire_id=b.inspire_id AND b.lsoa_11_cd = c.lsoa_11_cd AND a.inspire_id = d.inspire_id AND d.object_id = e.object_id AND c.postcode = '%s %s'" % (pc1, pc2))
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result


# Landfill Sites

class LandfillParcel(Resource):
    def get(self, inspire_id):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.hld_ref, e.site_name, e.site_add, e.ea_wmlr, e.regis_no, e.wrc_ref, e.bgs_num, e.site_ref, e.lic_hold, e.lic_hold_addr, e.site_op_name, e.site_op_addr, e.os_prefix, e.easting, e.northing, e.ea_region, e.ea_area, e.lic_issue, e.lic_surren, e.first_input, e.last_input, e.inert, e.industrial, e.commercial, e.household, e.special, e.liqsludge, e.wasteunk, e.gascontrol, e.leachatcnt, e.exempt, e.licensed, e.no_lic_reqd, e.buff_point, e.landfill_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_landfill d, landfill e WHERE a.inspire_id = d.inspire_id AND d.hld_ref = e.hld_ref AND a.inspire_id='%s'"%inspire_id)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class LandfillPostcode(Resource):
    def get(self, pc1, pc2):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.hld_ref, e.site_name, e.site_add, e.ea_wmlr, e.regis_no, e.wrc_ref, e.bgs_num, e.site_ref, e.lic_hold, e.lic_hold_addr, e.site_op_name, e.site_op_addr, e.os_prefix, e.easting, e.northing, e.ea_region, e.ea_area, e.lic_issue, e.lic_surren, e.first_input, e.last_input, e.inert, e.industrial, e.commercial, e.household, e.special, e.liqsludge, e.wasteunk, e.gascontrol, e.leachatcnt, e.exempt, e.licensed, e.no_lic_reqd, e.buff_point, e.landfill_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_lsoa b, lsoa c, mapping_landfill d, landfill e WHERE a.inspire_id=b.inspire_id  AND b.lsoa_11_cd = c.lsoa_11_cd AND a.inspire_id = d.inspire_id AND d.hld_ref = e.hld_ref AND c.postcode = '%s %s'" % (pc1, pc2))
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

#LSOA Detail

class LSOAParcel(Resource):
    def get(self, inspire_id):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, b.overlap_pc, c.lsoa_11_cd, c.lsoa_11_name, c.lsoa_11_name_w, c.postcode, c.in_use, c.latitude, c.longitude, c.easting, c.northing, c.grid_ref, c.county, c.district, c.ward, c.district_code, c.ward_code, c.country, c.country_code, c.constituency, c.introduced, c.terminated, c.parish, c.national_park, c.population, c.households, c.built_up_area, c.built_up_subdivision, c.lower_lsoa, c.rural_urban, c.region, c.altitude, c.lsoa_poly, c.area_sqkm, c.area_sqmi FROM inspire a, mapping_lsoa b, lsoa c WHERE a.inspire_id=b.inspire_id AND b.lsoa_11_cd = c.lsoa_11_cd AND a.inspire_id='%s'"%inspire_id)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class LSOAPostcode(Resource):
    def get(self, pc1, pc2):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, b.overlap_pc, c.lsoa_11_cd, c.lsoa_11_name, c.lsoa_11_name_w, c.postcode, c.in_use, c.latitude, c.longitude, c.easting, c.northing, c.grid_ref, c.county, c.district, c.ward, c.district_code, c.ward_code, c.country, c.country_code, c.constituency, c.introduced, c.terminated, c.parish, c.national_park, c.population, c.households, c.built_up_area, c.built_up_subdivision, c.lower_lsoa, c.rural_urban, c.region, c.altitude, c.lsoa_poly, c.area_sqkm, c.area_sqmi FROM inspire a, mapping_lsoa b, lsoa c WHERE a.inspire_id=b.inspire_id AND b.lsoa_11_cd = c.lsoa_11_cd AND c.postcode = '%s %s'" % (pc1, pc2))
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result


# PH & Bulk Density

class phbulkParcel(Resource):
    def get(self, inspire_id):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.phbulk_key, e.soil_group, e.lcm_class, e.lcm_number, e.dom_grain, e.caco3_rank, e.bulkd_07, e.bulkd_07se, e.ph_78, e.ph_78se, e.ph_98, e.ph_98se, e.ph_07, e.ph_07se, e.phbulk_poly e.area_sqkm, e.area_sqmi FROM inspire a, mapping_phbulk d, phbulk e WHERE a.inspire_id = d.inspire_id AND d.phbulk_key = e.phbulk_key AND a.inspire_id='%s'"%inspire_id)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class phbulkPostcode(Resource):
    def get(self, pc1, pc2):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.phbulk_key, e.soil_group, e.lcm_class, e.lcm_number, e.dom_grain, e.caco3_rank, e.bulkd_07, e.bulkd_07se, e.ph_78, e.ph_78se, e.ph_98, e.ph_98se, e.ph_07, e.ph_07se, e.phbulk_poly e.area_sqkm, e.area_sqmi FROM inspire a, mapping_lsoa b, lsoa c, mapping_phbulk d, phbulk e WHERE a.inspire_id=b.inspire_id AND b.lsoa_11_cd = c.lsoa_11_cd AND a.inspire_id = d.inspire_id AND d.phbulk_key = e.phbulk_key AND c.postcode = '%s %s'" % (pc1, pc2))
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

# Rail Noise

class railnoiseParcel(Resource):
    def get(self, inspire_id):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.rl_key, e.noise_class, e.rl_poly, e.area_sqkm, e.area_sqmi FROM inspire a,  mapping_railnoise d, rail_noise e WHERE a.inspire_id = d.inspire_id AND d.rl_key = e.rl_key AND a.inspire_id='%s'"%inspire_id)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class railnoisePostcode(Resource):
    def get(self, pc1, pc2):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.rl_key, e.noise_class, e.rl_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_lsoa b, lsoa c, mapping_railnoise d, rail_noise e WHERE a.inspire_id=b.inspire_id AND b.lsoa_11_cd = c.lsoa_11_cd AND a.inspire_id = d.inspire_id AND d.rl_key = e.rl_key AND c.postcode = '%s %s'" % (pc1, pc2))
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

# Road Noise

class roadnoiseParcel(Resource):
    def get(self, inspire_id):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.rd_key, e.noise_class, e.rd_poly, e.area_sqkm, e.area_sqmi FROM inspire a,  mapping_roadnoise d, road_noise e WHERE a.inspire_id = d.inspire_id AND d.rd_key = e.rd_key AND a.inspire_id='%s'"%inspire_id)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class roadnoisePostcode(Resource):
    def get(self, pc1, pc2):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.rd_key, e.noise_class, e.rd_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_lsoa b, lsoa c, mapping_roadnoise d, road_noise e WHERE a.inspire_id=b.inspire_id AND b.lsoa_11_cd = c.lsoa_11_cd AND a.inspire_id = d.inspire_id AND d.rd_key = e.rd_key AND c.postcode = '%s %s'" % (pc1, pc2))
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

# Soil PMM

class soilpmmParcel(Resource):
    def get(self, inspire_id):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.soilpmm_id, e.esb_desc, e.carb_cntnt, e.pmm_grain, e.soil_group, e.soil_tex, e.soil_depth, e.version, e.soil_ppm_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_soil_ppm d, soil_ppm e WHERE a.inspire_id = d.inspire_id AND d.soilpmm_id = e.soilpmm_id AND a.inspire_id='%s'"%inspire_id)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class soilpmmPostcode(Resource):
    def get(self, pc1, pc2):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.soilpmm_id, e.esb_desc, e.carb_cntnt, e.pmm_grain, e.soil_group, e.soil_tex, e.soil_depth, e.version, e.soil_ppm_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_lsoa b, lsoa c, mapping_soil_ppm d, soil_ppm e WHERE a.inspire_id=b.inspire_id AND b.lsoa_11_cd = c.lsoa_11_cd AND a.inspire_id = d.inspire_id AND d.soilpmm_id = e.soilpmm_id AND c.postcode = '%s %s'" % (pc1, pc2))
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result


# Topsoil Nutrients

class topsoilParcel(Resource):
    def get(self, inspire_id):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.cs_topsoil_key, e.lcm_class, e.lcm_number, e.dom_grain, e.soil_group, e.caco3_rank, e.cn_98, e.cn_98se, e.cn_07, e.cn_07se, e.nconc_98, e.nconc_98se, e.nconc_07, e.nconc_07se, e.olsen_98, e.olsen_98se, e.olsen_07, e.olsen_07se, e.topsoil_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_topsoil d, topsoil e WHERE a.inspire_id = d.inspire_id AND d.cs_topsoil_key = e.cs_topsoil_key AND a.inspire_id='%s'"%inspire_id)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class topsoilPostcode(Resource):
    def get(self, pc1, pc2):
        #Connect to database

	e = create_engine('sqlite:///db_landcat.sqlite')
        conn = e.connect()
        #Perform query and return JSON data
	query = conn.execute("SELECT distinct a.inspire_id, a.inspire_poly, d.overlap_pc, e.cs_topsoil_key, e.lcm_class, e.lcm_number, e.dom_grain, e.soil_group, e.caco3_rank, e.cn_98, e.cn_98se, e.cn_07, e.cn_07se, e.nconc_98, e.nconc_98se, e.nconc_07, e.nconc_07se, e.olsen_98, e.olsen_98se, e.olsen_07, e.olsen_07se, e.topsoil_poly, e.area_sqkm, e.area_sqmi FROM inspire a, mapping_lsoa b, lsoa c, mapping_topsoil d, topsoil e WHERE a.inspire_id=b.inspire_id AND b.lsoa_11_cd = c.lsoa_11_cd AND a.inspire_id = d.inspire_id AND d.cs_topsoil_key = e.cs_topsoil_key AND c.postcode = '%s %s'" % (pc1, pc2))
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result
                                
class HelloWorld(Resource):
	def get(self):
		test = 'hi there!'
		return test

		
# Adding the API resources
                       
api.add_resource(HelloWorld, '/hello')    

# Inspire Polygons 		

api.add_resource(InspireParcel, '/api/parcel/inspire/<string:inspire_id>')
api.add_resource(InspirePostcode, '/api/postcode/inspire/<string:pc1>/<string:pc2>')  
api.add_resource(InspireParcelPoly, '/api/parcel/inspire_poly/<string:inspire_id>')

# Land Classification

api.add_resource(ALCParcel, '/api/parcel/alc/<string:inspire_id>')
api.add_resource(ALCPostcode, '/api/postcode/alc/<string:pc1>/<string:pc2>')

# Conservation Areas

api.add_resource(ConservationParcel, '/api/parcel/conservation/<string:inspire_id>')
api.add_resource(ConservationPostcode, '/api/postcode/conservation/<string:pc1>/<string:pc2>')

# Contours

api.add_resource(ContoursParcel, '/api/parcel/contours/<string:inspire_id>')
api.add_resource(ContoursPostcode, '/api/postcode/contours/<string:pc1>/<string:pc2>')

# Flood Alerts

api.add_resource(FloodAlertsParcel, '/api/parcel/flood_alerts/<string:inspire_id>')
api.add_resource(FloodAlertsPostcode, '/api/postcode/flood_alerts/<string:pc1>/<string:pc2>')

#Flood Risks

api.add_resource(FloodRisksParcel, '/api/parcel/flood_risks/<string:inspire_id>')
api.add_resource(FloodRisksPostcode, '/api/postcode/flood_risks/<string:pc1>/<string:pc2>')

# Flood Warnings

api.add_resource(FloodWarningsParcel, '/api/parcel/flood_warnings/<string:inspire_id>')
api.add_resource(FloodWarningsPostcode, '/api/postcode/flood_warnings/<string:pc1>/<string:pc2>')

# Hydrogeology

api.add_resource(HydrogeologyParcel, '/api/parcel/hydrogeology/<string:inspire_id>')
api.add_resource(HydrogeologyPostcode, '/api/postcode/hydrogeology/<string:pc1>/<string:pc2>')


# Landfill Sites

api.add_resource(LandfillParcel, '/api/parcel/landfill/<string:inspire_id>')
api.add_resource(LandfillPostcode, '/api/postcode/landfill/<string:pc1>/<string:pc2>')


#LSOA Detail

api.add_resource(LSOAParcel, '/api/parcel/lsoa/<string:inspire_id>')
api.add_resource(LSOAPostcode, '/api/postcode/lsoa/<string:pc1>/<string:pc2>')


# PH & Bulk Density

api.add_resource(phbulkParcel, '/api/parcel/phbulk/<string:inspire_id>')
api.add_resource(phbulkPostcode, '/api/postcode/phbulk/<string:pc1>/<string:pc2>')

# Rail Noise

api.add_resource(railnoiseParcel, '/api/parcel/railnoise/<string:inspire_id>')
api.add_resource(railnoisePostcode, '/api/postcode/railnoise/<string:pc1>/<string:pc2>')

# Road Noise

api.add_resource(roadnoiseParcel, '/api/parcel/roadnoise/<string:inspire_id>')
api.add_resource(roadnoisePostcode, '/api/postcode/roadnoise/<string:pc1>/<string:pc2>')

# Soil PMM

api.add_resource(soilpmmParcel, '/api/parcel/soilpmm/<string:inspire_id>')
api.add_resource(soilpmmPostcode, '/api/postcode/soilpmm/<string:pc1>/<string:pc2>')

# Topsoil Nutrients

api.add_resource(topsoilParcel, '/api/parcel/topsoil/<string:inspire_id>')
api.add_resource(topsoilPostcode, '/api/postcode/topsoil/<string:pc1>/<string:pc2>')


if __name__ == '__main__':
    app.run(debug=True)

