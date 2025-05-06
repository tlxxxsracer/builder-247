import { Request, Response, NextFunction } from 'express';
import { validateSignature } from './signature_validation';

/**
 * Decorator to apply signature validation selectively
 * @param options Configuration for route validation
 */
export function ValidateRoute(options: {
  requireSignature?: boolean;
  skipEnvironments?: string[];
} = {}) {
  return function(
    target: any, 
    propertyKey: string, 
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    descriptor.value = async function(
      req: Request, 
      res: Response, 
      next: NextFunction
    ) {
      const { 
        requireSignature = true, 
        skipEnvironments = ['development', 'test'] 
      } = options;

      // Check if signature validation should be skipped
      if (
        requireSignature && 
        !skipEnvironments.includes(process.env.NODE_ENV || 'development')
      ) {
        try {
          await validateSignature(req, res, next);
        } catch (error) {
          return res.status(403).json({
            success: false,
            message: 'Route validation failed',
            error: error instanceof Error ? error.message : 'Unknown error'
          });
        }
      }

      // Call original method
      return originalMethod.apply(this, arguments);
    };

    return descriptor;
  };
}

/**
 * Global route validation configuration
 */
export const RouteValidationConfig = {
  /**
   * List routes that should always be exempt from signature validation
   */
  exemptRoutes: [
    '/hello',
    '/health',
    '/prometheus/info',
    '/docs/signature-generation'
  ],

  /**
   * Check if a route should be validated
   * @param route Route path
   * @returns Boolean indicating if route needs validation
   */
  shouldValidateRoute: (route: string): boolean => {
    return !RouteValidationConfig.exemptRoutes.some(
      exemptRoute => route.startsWith(exemptRoute)
    );
  }
};