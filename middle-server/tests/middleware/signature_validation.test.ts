import { Request, Response, NextFunction } from 'express';
import { validateSignature } from '../../src/middleware/signature_validation';
import * as signUtils from '../../src/utils/sign';
import nacl from 'tweetnacl';
import bs58 from 'bs58';

jest.mock('../../src/utils/sign');

describe('Signature Validation Middleware', () => {
  let mockReq: Partial<Request>;
  let mockRes: Partial<Response>;
  let mockNext: NextFunction;

  beforeEach(() => {
    // Generate a mock keypair
    const keypair = nacl.sign.keyPair();
    const stakingKey = bs58.encode(keypair.publicKey);
    const body = { test: 'data' };

    mockReq = {
      headers: {
        signature: '',
        stakingKey: stakingKey
      },
      body: body
    };

    mockRes = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };

    mockNext = jest.fn();

    // Mock verifySignature to use the actual implementation during tests
    (signUtils.verifySignature as jest.Mock) = jest.fn().mockImplementation(
      async (signature, key) => {
        return { data: JSON.stringify(body) };
      }
    );
  });

  it('should pass when signature is valid', async () => {
    mockReq.headers!.signature = 'valid_signature';

    await validateSignature(
      mockReq as Request, 
      mockRes as Response, 
      mockNext
    );

    expect(mockNext).toHaveBeenCalled();
    expect(mockRes.status).not.toHaveBeenCalled();
  });

  it('should fail when signature is missing', async () => {
    delete mockReq.headers!.signature;

    await validateSignature(
      mockReq as Request, 
      mockRes as Response, 
      mockNext
    );

    expect(mockRes.status).toHaveBeenCalledWith(400);
    expect(mockNext).not.toHaveBeenCalled();
  });

  it('should fail when stakingKey is missing', async () => {
    delete mockReq.headers!.stakingKey;
    mockReq.headers!.signature = 'valid_signature';

    await validateSignature(
      mockReq as Request, 
      mockRes as Response, 
      mockNext
    );

    expect(mockRes.status).toHaveBeenCalledWith(400);
    expect(mockNext).not.toHaveBeenCalled();
  });

  it('should fail when signature verification fails', async () => {
    (signUtils.verifySignature as jest.Mock).mockResolvedValue({
      error: 'Invalid signature'
    });

    mockReq.headers!.signature = 'invalid_signature';

    await validateSignature(
      mockReq as Request, 
      mockRes as Response, 
      mockNext
    );

    expect(mockRes.status).toHaveBeenCalledWith(403);
    expect(mockNext).not.toHaveBeenCalled();
  });
});