SELECT *
FROM service_feed as sf, service_feed_entry as sfe, dataset_feed as df
WHERE sf.pkuid = sfe.sf_id
AND sfe.pkuid = df.sfe_id