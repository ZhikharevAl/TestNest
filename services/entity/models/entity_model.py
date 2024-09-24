from pydantic import BaseModel, Field


class AdditionRequest(BaseModel):
    """Model representing additional information for an entity request."""

    additional_info: str | None = Field(None, description="additionalEntityDetails")
    additional_number: int | None = Field(None, description="additionalNumberForEntity")


class EntityRequest(BaseModel):
    """Model for sending entity data in a request."""

    title: str = Field(..., description="entityTitle")
    verified: bool = Field(..., description="entityVerificationStatus")
    important_numbers: list[int] = Field(
        ..., description="anArrayOfImportantNumbersForTheEntity"
    )
    addition: AdditionRequest | None = Field(
        None, description="additionalInformationAboutTheEvent"
    )


class AdditionResponse(BaseModel):
    """Model representing additional information for an entity in a response."""

    id: int = Field(..., description="additionalInformationID")
    additional_info: str | None = Field(None, description="additionalEntityDetails")
    additional_number: int | None = Field(None, description="additionalNumberForEntity")


class EntityResponse(BaseModel):
    """Model for receiving entity data in a response."""

    id: int = Field(..., description="entityID")
    title: str = Field(..., description="entityTitle")
    verified: bool = Field(..., description="entityVerificationStatus")
    important_numbers: list[int] = Field(
        ..., description="anArrayOfImportantNumbersForTheEntity"
    )
    addition: AdditionResponse | None = Field(
        None, description="additionalInformationAboutTheEntity"
    )
