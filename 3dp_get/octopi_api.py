api_key = "3F20D906D78C439B9FAD11F9AB270E18"

account = {
    'id' : "vcml_yonsei",
    'pw' : "still alive"
}

octopi_spec = {
    "status" : {
        "path" : "/api/printer"
    },
    
    "head" : {
        "path" : "/api/printer"
    },

    "bed" : {
        "path" : "/api/printer"
    }
}

octopi_query = {
    "create_table" : "CREATE TABLE IF NOT EXISTS octopi (id integer PRIMARY KEY, time_stamp text, stat text, ext1_temp float, bed_temp float)",
    "insert_table" : "insert into octopi (time_stamp, stat, ext1_temp, bed_temp) VALUES (?, ?, ?, ?)"
}