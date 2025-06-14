import traceback
try:
    from backend.models.user import Assessment
    from backend.schemas.assessment import AssessmentOut
    
    assessment = Assessment()
    print("Assessment attributes:", vars(assessment))
    
    # Test converting assessment to dictionary
    test_assessment = Assessment(
        id=1,
        user_id=1,
        type="test",
        data={"test": "data"},
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00"
    )
    
    # Test the assessment model to see what's wrong
    print("\nTest assessment:", vars(test_assessment))
    
    # Try to simulate what happens in the endpoint
    assessments = [test_assessment]
    print("\nTrying to convert to schema:")
    for assessment in assessments:
        # See if we can convert to a dict
        assessment_dict = {c.name: getattr(assessment, c.name) for c in assessment.__table__.columns}
        print(assessment_dict)
        
        # Try to create an AssessmentOut from this
        assessment_out = AssessmentOut.from_orm(assessment)
        print(assessment_out.dict())
        
except Exception as e:
    traceback.print_exc()
