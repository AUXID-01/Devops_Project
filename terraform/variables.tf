variable "aws_region" {
  type        = string
  description = "AWS Region to deploy resources"
  default     = "us-east-1"
}

variable "environment" {
  type        = string
  description = "Environment name (e.g., dev, prod)"
  default     = "dev"
}

variable "cluster_name" {
  type        = string
  description = "Name of the EKS cluster"
  default     = "bugboard-eks"
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  type        = list(string)
  description = "CIDR blocks for the public subnets"
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  type        = list(string)
  description = "CIDR blocks for the private subnets"
  default     = ["10.0.10.0/24", "10.0.20.0/24"]
}

variable "node_instance_types" {
  type        = list(string)
  description = "List of EC2 instance types for the EKS node group"
  default     = ["t3.medium"]
}

variable "desired_capacity" {
  type        = number
  description = "Desired number of worker nodes"
  default     = 2
}

variable "min_capacity" {
  type        = number
  description = "Minimum number of worker nodes"
  default     = 1
}

variable "max_capacity" {
  type        = number
  description = "Maximum number of worker nodes"
  default     = 3
}
