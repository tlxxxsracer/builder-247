import { Request, Response, NextFunction } from 'express';
import { validateSignature, getSignatureGenerationDocs } from '../../src/middleware/signature_validation';
import * as signUtils from '../../src/utils/sign';

// Mock the sign utility
jest.mock('../../src/utils/sign');

describe('Signature Validation Middleware', () => {
  let mockReq: Partial<Request>;
  let mockRes: Partial<Response>;
  let mockNext: NextFunction;

  beforeEach(() => {
    process.env.DISABLE_SIGNATURE_VALIDATION = 'false';
    
    mockReq = {
      headers: {
        signature: 'valid_signature',
        stakingkey: 'valid_key'
      },
      body: { test: 'data' }
    };

    mockRes = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };

    mockNext = jest.fn();

    // Default mock implementation
    (signUtils.verifySignature as jest.Mock).mockResolvedValue({
      data: JSON.stringify({ test: 'data' })
    });
  });

  afterEach(() => {
    delete process.env.DISABLE_SIGNATURE_VALIDATION;
    delete process.env.STRICT_PAYLOAD_VALIDATION;
  });

  it('should pass when signature is valid', async () => {
    await validateSignature(
      mockReq as Request, 
      mockRes as Response, 
      mockNext
    );

    expect(mockNext).toHaveBeenCalled();
    expect(mockRes.status).not.toHaveBeenCalled();
  });

  it('should bypass validation when DISABLE_SIGNATURE_VALIDATION is true', async () => {
    process.env.DISABLE_SIGNATURE_VALIDATION = 'true';

    await validateSignature(
      mockReq as Request, 
      mockRes as Response, 
      mockNext
    );

    expect(mockNext).toHaveBeenCalled();
  });

  it('should fail when signature is missing', async () => {
    delete mockReq.headers!.signature;

    await validateSignature(
      mockReq as Request, 
      mockRes as Response, 
      mockNext
    );

    expect(mockRes.status).toHaveBeenCalledWith(400);
    expect(mockRes.json).toHaveBeenCalledWith(expect.objectContaining({
      code: 'MISSING_SIGNATURE'
    }));
  });

  it('should fail when stakingkey is missing', async () => {
    delete mockReq.headers!.stakingkey;

    await validateSignature(
      mockReq as Request, 
      mockRes as Response, 
      mockNext
    );

    expect(mockRes.status).toHaveBeenCalledWith(400);
    expect(mockRes.json).toHaveBeenCalledWith(expect.objectContaining({
      code: 'MISSING_SIGNATURE'
    }));
  });

  it('should handle signature verification failures', async () => {
    (signUtils.verifySignature as jest.Mock).mockResolvedValue({
      error: 'Invalid signature'
    });

    await validateSignature(
      mockReq as Request, 
      mockRes as Response, 
      mockNext
    );

    expect(mockRes.status).toHaveBeenCalledWith(403);
    expect(mockRes.json).toHaveBeenCalledWith(expect.objectContaining({
      code: 'INVALID_SIGNATURE'
    }));
  });

  it('should handle payload mismatch when strict validation is enabled', async () => {
    process.env.STRICT_PAYLOAD_VALIDATION = 'true';
    (signUtils.verifySignature as jest.Mock).mockResolvedValue({
      data: JSON.stringify({ different: 'payload' })
    });

    await validateSignature(
      mockReq as Request, 
      mockRes as Response, 
      mockNext
    );

    expect(mockRes.status).toHaveBeenCalledWith(403);
    expect(mockRes.json).toHaveBeenCalledWith(expect.objectContaining({
      code: 'PAYLOAD_MISMATCH'
    }));
  });

  it('should provide signature generation documentation', () => {
    const docs = getSignatureGenerationDocs();
    
    expect(docs).toHaveProperty('description');
    expect(docs).toHaveProperty('steps');
    expect(docs).toHaveProperty('example');
  });
});