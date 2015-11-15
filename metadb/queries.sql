SELECT  df.title || ' ' ||  dfe.srs_auth || ':' || dfe.srs_code || ' (' || dfe.format_txt || ')' as title,
 dfe.alternate_link, dfe.summary, dfe.format_mime, dfe.format_txt, dfe.srs_auth, dfe.srs_code, dfe.srs_txt, dfe.updated,
 sfe.x_min
FROM service_feed_entry as sfe, dataset_feed as df, dataset_feed_entry as dfe
WHERE sfe.identifier_code = '788f4376-a625-4c0a-8704-458aa59bff79'
AND sfe.pkuid = df.sfe_id
AND df.pkuid = dfe.df_id
