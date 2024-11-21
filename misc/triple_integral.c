#include <stdio.h>
#include <stdlib.h>
#define _USE_MATH_DEFINES
#include <math.h>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

typedef struct {
    double x, y, z;
} Point;

typedef struct {
    double r1, r2, t1, t2, p1, p2;
} Space;

typedef struct {
    int nr, nt, np;
} Resolution;

typedef struct {
    double dr, dt, dp;
    Point *points;
    int num_points;
} Domain;

double delta(double a, double b, int n) {
    return (b - a) / n;
}

void interval(double a, double d, int n, double *result) {
    for (int i = 0; i < n; i++) {
        result[i] = a + d * i;
    }
}

double normr(double r) {
    return r < 0 ? 0 : r;
}

double normt(double t) {
    while (t < 0) t += 2 * M_PI;
    while (t >= 2 * M_PI) t -= 2 * M_PI;
    return t;
}

double normp(double p) {
    if (p < 0) return 0;
    if (p > M_PI) return M_PI;
    return p;
}

Domain createDomain(Space space, Resolution res) {
    Domain domain;
    domain.num_points = res.nr * res.nt * res.np;
    domain.points = (Point *)malloc(domain.num_points * sizeof(Point));
    if (domain.points == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }
    
    domain.dr = delta(space.r1, space.r2, res.nr);
    domain.dt = delta(space.t1, space.t2, res.nt);
    domain.dp = delta(space.p1, space.p2, res.np);
    
    double *rr = (double *)malloc(res.nr * sizeof(double));
    double *tt = (double *)malloc(res.nt * sizeof(double));
    double *pp = (double *)malloc(res.np * sizeof(double));
    
    if (rr == NULL || tt == NULL || pp == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        free(rr);
        free(tt);
        free(pp);
        free(domain.points);
        exit(EXIT_FAILURE);
    }
    
    interval(space.r1, domain.dr, res.nr, rr);
    interval(space.t1, domain.dt, res.nt, tt);
    interval(space.p1, domain.dp, res.np, pp);
    
    int index = 0;
    for (int i = 0; i < res.nr; i++) {
        for (int j = 0; j < res.nt; j++) {
            for (int k = 0; k < res.np; k++) {
                domain.points[index++] = (Point){rr[i], tt[j], pp[k]};
            }
        }
    }
    
    free(rr);
    free(tt);
    free(pp);
    
    return domain;
}

double getVolume(Domain domain, Point p) {
    return p.x * p.x * sin(p.z) * domain.dr * domain.dt * domain.dp;
}

Point *getPoints(Domain domain) {
    return domain.points;
}

double integrate(Domain domain, int (*predicate)(Point), double (*function)(Point)) {
    double sum = 0;
    for (int i = 0; i < domain.num_points; i++) {
        Point p = domain.points[i];
        if (predicate(p)) {
            sum += function(p) * getVolume(domain, p);
        }
    }
    return sum;
}

int predicate(Point p) {
    return 1; // Integrate over all points
}

double function(Point p) {
    return 1;
}

void freeDomain(Domain *domain) {
    free(domain->points);
    domain->points = NULL;
    domain->num_points = 0;
}

int main() {
    Space space = {0, 3, 0, 2 * M_PI, 0, M_PI};
    Resolution res = {100, 200, 200};

    Domain domain = createDomain(space, res);

    double volume = integrate(domain, predicate, function);
    printf("Calculated volume: %f\n", volume);

    freeDomain(&domain);
    return 0;
}