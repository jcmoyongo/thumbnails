output "container_app_url" {
  value = azurerm_container_app.app.latest_revision_fqdn
}

output "storage_connection_string" {
  value = azurerm_storage_account.storage.primary_connection_string
  sensitive = true
}