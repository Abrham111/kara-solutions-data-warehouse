WITH raw_data AS (
  SELECT 
    sender, 
    id, 
    content,
    timestamp,
    -- Use LATERAL join to extract URLs
    ARRAY_AGG(urls.url) AS links,
    -- Use LATERAL join to extract emojis
    ARRAY_AGG(emojis.emoji) AS emojis,
    -- Clean content by removing URLs and emojis
    REGEXP_REPLACE(REGEXP_REPLACE(content, 'https?://\S+', ''), '[\p{So}\p{Cn}]', '') AS clean_content
  FROM 
    {{ source('raw', 'raw_telegram_data') }} t
  LEFT JOIN LATERAL (
    SELECT unnest(REGEXP_MATCHES(content, 'https?://\S+', 'g')) AS url
  ) AS urls ON true
  LEFT JOIN LATERAL (
    SELECT unnest(REGEXP_MATCHES(content, '[\p{So}\p{Cn}]', 'g')) AS emoji
  ) AS emojis ON true
  GROUP BY 
    sender, id, content, timestamp
)

SELECT 
  sender, 
  id, 
  clean_content AS content,  -- Cleaned content (without URLs and emojis)
  links, 
  emojis, 
  timestamp::TIMESTAMP AS timestamp  -- Convert to timestamp
FROM 
  raw_data
