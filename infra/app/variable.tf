variable "app_name" {
  description = "Name of the app."
  type        = string
}
variable "region" {
  description = "AWS region to deploy the network to."
  type        = string
}
variable "image" {
  description = "Image used to start the container. Should be in repository-url/image:tag format."
  type        = string
}
variable "aws_access_key_id" {
  description = "AWS access key ID."
  type        = string
}
variable "aws_secret_access_key" {
  description = "AWS secret access key."
  type        = string
}
variable "jwt_secret" {
  description = "JWT secret for authentication."
  type        = string
}
variable "client_id" {
  description = "Client ID for the application."
  type        = string
}
variable "client_secret" {
  description = "Client secret for the application."
  type        = string
}
variable "table_name" {
  description = "Name of the DynamoDB table."
  type        = string
}