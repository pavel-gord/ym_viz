CREATE DATABASE IF NOT EXISTS yam;

USE yam;
CREATE TABLE IF NOT EXISTS yam_site (
        date Date,      
        trafficSource String,
        socialNetwork String,
        deviceCategory String,
        operatingSystemRoot String,
        browser String,
        visits UInt32,
        pageviews UInt32,
        users UInt32,
        manPercentage Float32,
        under18AgePercentage Float32,
        over44AgePercentage Float32
        ) ENGINE = MergeTree()
        PARTITION BY toYYYYMM(date)
        ORDER BY (date, trafficSource, socialNetwork, deviceCategory, operatingSystemRoot, browser);