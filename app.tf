resource "azurerm_container_app_environment" "env" {
  name                = "thumbapp-env"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_container_app" "app" {
  name                = "thumbnail-generator"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name = azurerm_resource_group.rg.name

  revision_mode       = "Single"

  template {
    container {
      name   = "thumbgen"
      image  = "${azurerm_container_registry.acr.login_server}/thumb_nails:latest"
      memory = "1.0Gi"
      cpu    = 0.5

      env {
        name  = "AZURE_STORAGE_CONNECTION_STRING"
        value = azurerm_storage_account.storage.primary_connection_string
      }

    }

  }

  ingress {
    external_enabled = true
    target_port      = 80

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  registry {
    server   = azurerm_container_registry.acr.login_server
  }
}