variable "gcp_project_id" {
  description = "Google Cloud Project ID"
  type        = string
  default     = "paypulse-fintech-demo"
}

variable "gcp_region" {
  description = "GCP Region for cloud resources"
  type        = string
  default     = "us-central1"
}

variable "bigquery_dataset_raw" {
  description = "BigQuery raw landing dataset name"
  type        = string
  default     = "fintech_raw"
}

variable "bigquery_dataset_analytics" {
  description = "BigQuery analytics mart dataset name"
  type        = string
  default     = "fintech_analytics"
}
