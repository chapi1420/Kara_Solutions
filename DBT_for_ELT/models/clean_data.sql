WITH raw_data AS (
    SELECT * FROM {{ source('staging', '/home/nahomnadew/Desktop/10x/week7/Kara_Solutions/data/cleaned_telegram_data.csv') }}
)

SELECT DISTINCT
    LOWER(trim(name)) AS name,
    LOWER(trim(address)) AS address,
    COALESCE(phone, 'Unknown') AS phone,
    COALESCE(email, 'Unknown') AS email,
    CAST(date AS DATE) AS cleaned_date
FROM raw_data
WHERE name IS NOT NULL;
