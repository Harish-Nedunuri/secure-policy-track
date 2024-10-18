# main.tf

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  required_version = ">= 1.0.0"
}

provider "azurerm" {
  features {}
}

# 1. Create a Resource Group in UK South
resource "azurerm_resource_group" "rg" {
  name     = "secure-policy-rg"
  location = "UK South"

  tags = {
    environment = "dev"
    project     = "secure-policy-track"
    deployment  = "terraform"
  }
}


# 3. Create an Azure Container Registry
resource "azurerm_container_registry" "acr" {
  name                = var.container_registry_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true

  tags = {
    environment = "dev"
    project     = "secure-policy-track"
    deployment  = "terraform"
  }
}
