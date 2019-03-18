um3_spec = {
    "auth" : {
       "register" : {"path" : "/api/v1/auth/request"},
       "check" : {"path" : "/api/v1/auth/check"}
    },

    "status" : {
        "path" : "/api/v1/printer/status"
    },
    
    "head" : {
        "path" : "/api/v1/printer/heads"
    },

    "bed" : {
        "path" : "/api/v1/printer/bed"
    }
}

um3_query = {
    "create_table" : "CREATE TABLE IF NOT EXISTS um3 (id integer PRIMARY KEY, time_stamp text, stat text, ext1_temp float, ext2_temp float, bed_temp float)",
    "insert_table" : "insert into um3 (time_stamp, stat, ext1_temp, ext2_temp, bed_temp) VALUES (?, ?, ?, ?, ?)"
}