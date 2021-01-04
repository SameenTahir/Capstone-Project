class SqlQueries:
    immigration_data_insert = ("""
        INSERT INTO pblic.immigration_data_insert (
				id 
				,cicid 
				,i94yr
				,i94mon 
				,i94cit 
				,i94res 
				,i94port
				,arrdate
				,i94mode
				,i94addr
				,depdate
				,i94bir 
				,i94visa
				,_COUNT 
				,dtadfile
				,visapost
				,occup 
				,entdepa 
				,entdepd 
				,entdepu 
				,matflag 
				,biryear 
				,dtaddto 
				,gender 
				,insnum 
				,airline 
				,admnum 
				,fltno 
				,visatype 

        )
        SELECT
				id 
				,cicid 
				,i94yr
				,i94mon 
				,i94cit 
				,i94res 
				,i94port
				,arrdate
				,i94mode
				,i94addr
				,depdate
				,i94bir 
				,i94visa
				,_COUNT 
				,dtadfile
				,visapost
				,occup 
				,entdepa 
				,entdepd 
				,entdepu 
				,matflag 
				,biryear 
				,dtaddto 
				,gender 
				,insnum 
				,airline 
				,admnum 
				,fltno 
				,visatype 
				FROM public.immigration_data_stg
				;

    """)

    airport_codes_table_insert = ("""
        INSERT INTO public.dim_airport_codes (
						ident,
						type, 
						elevation_ft,
						continent,
						iso_country,
						iso_region,
						municipality,
						gps_code,
						iata_code,
						local_code,
						coordinates

        )
        SELECT 
						SUBSTR(ident,2) AS ident_1
						type, 
						elevation_ft,
						continent,
						iso_country,
						iso_region,
						municipality,
						gps_code,
						iata_code,
						local_code,
						coordinates

        FROM public.airport_codes_Stg
    """)

    visatype_table_insert= ("""
        INSERT INTO public.dim_visa_type (
            visa_type_id,
            visa_type
        )
		VALUES
		(
		1,Business
		)
    """)

    date_hierarchy_table_insert = ("""
        INSERT INTO public.dim_Date_Hierarchy (
            Date_key,
            Date_val,
            Month_Val,
            Year_Val
        )
			SELECT TO_CHAR(datum,'yyyymmdd')::INT AS date_key,
				   datum AS date_actual,
				   EXTRACT(MONTH FROM datum) AS month_key,
				   EXTRACT(isoyear FROM datum) AS year_key,
			FROM (SELECT '1970-01-01'::DATE+ SEQUENCE.DAY AS datum
				  FROM GENERATE_SERIES (0,29219) AS SEQUENCE (DAY)
				  GROUP BY SEQUENCE.DAY) DQ
			""")
