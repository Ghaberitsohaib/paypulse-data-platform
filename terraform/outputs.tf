output "lakehouse_bucket_url" {
  description = "GCS Data Lakehouse URL"
  value       = google_storage_bucket.paypulse_lakehouse.url
}

output "raw_dataset_id" {
  description = "BigQuery Raw Dataset ID"
  value       = google_bigquery_dataset.fintech_raw.dataset_id
}

output "analytics_dataset_id" {
  description = "BigQuery Analytics Dataset ID"
  value       = google_bigquery_dataset.fintech_analytics.dataset_id
}
