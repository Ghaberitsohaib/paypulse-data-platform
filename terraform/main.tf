terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

resource "google_storage_bucket" "paypulse_lakehouse" {
  name          = "${var.gcp_project_id}-paypulse-lakehouse"
  location      = var.gcp_region
  force_destroy = true

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "SetStorageClass"
      storage_class = "NEARLINE"
    }
    condition {
      age = 90
    }
  }
}

resource "google_bigquery_dataset" "fintech_raw" {
  dataset_id                  = var.bigquery_dataset_raw
  friendly_name               = "PayPulse Raw Ingestion"
  description                 = "Landing dataset for streaming payment events and currency exchange rates"
  location                    = var.gcp_region
  default_table_expiration_ms = null

  labels = {
    env    = "production"
    domain = "fintech_payments"
  }
}

resource "google_bigquery_dataset" "fintech_analytics" {
  dataset_id                  = var.bigquery_dataset_analytics
  friendly_name               = "PayPulse Financial Analytics Marts"
  description                 = "Dimensional models, merchant settlements, and anti-money laundering alerts"
  location                    = var.gcp_region
  default_table_expiration_ms = null

  labels = {
    env    = "production"
    domain = "analytics_engineering"
  }
}
