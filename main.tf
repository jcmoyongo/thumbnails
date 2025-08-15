provider "azurerm" {
  features {}
  subscription_id = "6718374f-b840-4843-b17e-d493fe14f3ca"
}

resource "azurerm_resource_group" "rg" {
  name     = "thumbnail-lab-rg"
  location = "East US"
}

resource "azurerm_storage_account" "storage" {
  name                     = "thumbstor${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "container" {
  name                  = "thumbnails"
  storage_account_id    = azurerm_storage_account.storage.id
  container_access_type = "private"
}

resource "random_string" "suffix" {
  length  = 6
  upper   = false
  numeric  = true
  special = false
}

resource "azurerm_container_registry" "acr" {
  name                = "thumbnailacr${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true
}